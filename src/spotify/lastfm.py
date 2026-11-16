"""Cached Last.fm (and Spotify oEmbed) client for the spotify data loaders.

Every response is stored in $SPOTIFY_CACHE_DIR/lastfm.sqlite, so a build only calls the
API for artists, tracks and genres it has not seen (or whose entry has expired). The
cache file is the thing to copy between machines; it holds no credentials. Scrobbles are
kept in the same file and synced incrementally.

The first build after a new export can need thousands of calls (about 3 per new artist at
Last.fm's 5/s limit), so warm the cache ahead of time:
    uv run src/spotify/lastfm.py warm
"""

import json
import os
import re
import sqlite3
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

API = "https://ws.audioscrobbler.com/2.0/"
OEMBED = "https://open.spotify.com/oembed"
USER_AGENT = "beehive-spotify/1.0 (+https://wasabipesto.com/spotify/)"
MIN_INTERVAL = 0.25  # seconds between calls; Last.fm asks for at most 5/s averaged
NOT_FOUND = 6  # Last.fm error code for an unknown artist/track/tag
TRANSIENT = {8, 11, 16, 29}  # operation failed, service offline, temporary error, rate limited
DAY = 86400


def squash(name: str) -> str:
    """Name reduced to ASCII letters and digits, for "same name, different punctuation"."""
    ascii_ = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^0-9a-z]", "", ascii_.casefold())


class LastFM:
    def __init__(self, cache_dir: str | os.PathLike | None = None, api_key: str | None = None, offline: bool = False):
        cache_dir = Path(cache_dir or os.environ["SPOTIFY_CACHE_DIR"]).expanduser()
        cache_dir.mkdir(parents=True, exist_ok=True)
        self.api_key = api_key or os.environ.get("LASTFM_API_KEY")
        self.db = sqlite3.connect(cache_dir / "lastfm.sqlite")
        self.db.executescript(
            "CREATE TABLE IF NOT EXISTS responses ("
            " method TEXT NOT NULL, key TEXT NOT NULL, fetched_at INTEGER NOT NULL,"
            " body TEXT NOT NULL, PRIMARY KEY (method, key));"
            "CREATE TABLE IF NOT EXISTS scrobbles ("
            " uts INTEGER NOT NULL, artist TEXT NOT NULL, track TEXT NOT NULL, album TEXT,"
            " PRIMARY KEY (uts, artist, track));"
        )
        self._last_call = 0.0
        self.calls = 0
        # Answer from the cache only (misses look like "not found"); also set by LASTFM_OFFLINE=1.
        self.offline = offline or os.environ.get("LASTFM_OFFLINE") == "1"

    # --- transport ---------------------------------------------------------------------

    def _throttle(self):
        wait = self._last_call + MIN_INTERVAL - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self._last_call = time.monotonic()
        self.calls += 1

    def _fetch(self, method: str, params: dict) -> dict:
        if not self.api_key:
            raise RuntimeError("LASTFM_API_KEY is not set and the cache has no entry for this request")
        # Last.fm decodes the query string twice, so a literal "+" must be sent as %252B;
        # sent once-encoded, "Florence + The Machine" resolves to a different artist.
        query = urllib.parse.urlencode(
            {**params, "method": method, "api_key": self.api_key, "format": "json"}, quote_via=urllib.parse.quote
        ).replace("%2B", "%252B")
        for attempt in range(6):
            self._throttle()
            try:
                req = urllib.request.Request(f"{API}?{query}", headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=30) as r:
                    body = json.load(r)
            except urllib.error.HTTPError as e:
                try:
                    body = json.load(e)
                except ValueError:
                    body = {"error": -e.code, "message": str(e)}
            except (urllib.error.URLError, TimeoutError, ValueError) as e:
                body = {"error": -1, "message": str(e)}
            err = body.get("error")
            if err is None or err == NOT_FOUND:
                return body
            if err in TRANSIENT or err < 0:
                time.sleep(min(60, 2**attempt))
                continue
            raise RuntimeError(f"Last.fm {method} {params}: {body}")  # bad key, bad params, suspended...
        raise RuntimeError(f"Last.fm {method} {params}: gave up after retries: {body}")

    def _cached(self, method: str, params: dict, max_age_days: float, fetch) -> dict:
        key = json.dumps({k: str(v).lower() for k, v in sorted(params.items())}, ensure_ascii=False)
        row = self.db.execute("SELECT fetched_at, body FROM responses WHERE method=? AND key=?", (method, key)).fetchone()
        if row and (self.offline or time.time() - row[0] < max_age_days * DAY):
            return json.loads(row[1])
        if self.offline:
            return {}
        body = fetch()
        self.db.execute("INSERT OR REPLACE INTO responses VALUES (?, ?, ?, ?)", (method, key, int(time.time()), json.dumps(body)))
        self.db.commit()
        return body

    def get(self, method: str, max_age_days: float = 180, **params) -> dict:
        """Cached Last.fm call. Not-found answers are cached too, so they aren't retried every night."""
        return self._cached(method, params, max_age_days, lambda: self._fetch(method, params))

    # --- artists -----------------------------------------------------------------------

    def _info(self, name, autocorrect):
        return self.get("artist.getInfo", artist=name, autocorrect=autocorrect).get("artist")

    def artist(self, name: str) -> dict | None:
        """Resolve a Spotify artist name to Last.fm listeners, tags and similar artists.

        Autocorrect is right for spelling variants (STRFKR -> Starfucker) but sometimes picks
        a different artist (KIRA -> KiraÇ, Noah Cyrus -> Miley Cyrus). When the corrected name
        differs beyond punctuation, the exact-name page decides: alias pages exist (they collect
        Spotify's scrobbles, so they have the better listener count) but carry no tags, while a
        real artist page has tags and means the correction was wrong.
        """
        name = " ".join(name.split())  # Spotify has names like "Super City " with stray spaces
        corrected = self._info(name, 1)
        ac = 1
        listeners_from = corrected
        fold = lambda s: unicodedata.normalize("NFKC", s).casefold().strip()
        same = corrected and (
            fold(corrected["name"]) == fold(name) or (squash(name) and squash(corrected["name"]) == squash(name))
        )
        if not same:
            exact = self._info(name, 0)
            if exact:
                listeners_from = exact
                if exact.get("tags", {}).get("tag") or not corrected:
                    ac = 0
        page = self._info(name, ac)
        if not page:
            return None
        tags = self.get("artist.getTopTags", artist=name, autocorrect=ac).get("toptags", {}).get("tag", [])
        similar = self.get("artist.getSimilar", artist=name, autocorrect=ac, limit=100).get("similarartists", {}).get("artist", [])
        return {
            "name": page["name"],
            "listeners": int(listeners_from["stats"]["listeners"]),
            "tags": [(t["name"], int(t["count"])) for t in tags],
            "similar": [(s["name"], float(s["match"])) for s in similar],
        }

    # --- tracks, tags, covers ----------------------------------------------------------

    def track(self, artist: str, track: str) -> dict | None:
        t = self.get("track.getInfo", artist=artist, track=track, autocorrect=1).get("track")
        if not t:
            return None
        images = t.get("album", {}).get("image", [])
        return {
            "listeners": int(t.get("listeners", 0)),
            "duration_ms": int(t.get("duration") or 0),
            "image": next((i["#text"] for i in reversed(images) if i.get("#text")), None),
        }

    def tag_reach(self, tag: str) -> int:
        """Number of Last.fm users who have used a tag; 0 if it isn't a tag there."""
        t = self.get("tag.getInfo", tag=tag).get("tag") or {}
        return int(t.get("reach", 0) or 0)

    def spotify_cover(self, track_uri: str) -> str | None:
        """Album art URL for a Spotify track, via oEmbed (no Spotify credentials needed)."""

        def fetch():
            self._throttle()
            url = f"{OEMBED}?{urllib.parse.urlencode({'url': track_uri})}"
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": USER_AGENT}), timeout=30) as r:
                    return {"thumbnail_url": json.load(r).get("thumbnail_url")}
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    return {"thumbnail_url": None}
                raise

        return self._cached("spotify.oembed", {"uri": track_uri}, 365, fetch).get("thumbnail_url")

    # --- scrobbles ---------------------------------------------------------------------

    def sync_scrobbles(self, user: str):
        """Fetch scrobbles newer than the newest one stored."""
        if self.offline:
            return
        newest = self.db.execute("SELECT max(uts) FROM scrobbles").fetchone()[0] or 0
        page, pages = 1, 1
        while page <= pages:
            body = self._fetch("user.getRecentTracks", {"user": user, "from": newest + 1, "limit": 200, "page": page})
            rt = body.get("recenttracks", {})
            pages = int(rt.get("@attr", {}).get("totalPages", 0) or 0)
            rows = [
                (int(t["date"]["uts"]), t["artist"]["#text"], t["name"], t.get("album", {}).get("#text"))
                for t in rt.get("track", [])
                if "date" in t  # the now-playing entry has no date yet
            ]
            self.db.executemany("INSERT OR IGNORE INTO scrobbles VALUES (?, ?, ?, ?)", rows)
            self.db.commit()
            page += 1

    def scrobbles(self, since: int = 0):
        return self.db.execute("SELECT uts, artist, track, album FROM scrobbles WHERE uts > ? ORDER BY uts", (since,)).fetchall()


def warm():
    """Fill the cache for everything the loaders will ask for, most important first."""
    sys.path.insert(0, str(Path(__file__).parent))
    import genres
    import listening
    from takeout import load_plays

    plays = listening.recent(load_plays())
    fm = LastFM()
    t0 = time.time()

    def progress(what, i, n):
        if i % 250 == 0 or i == n:
            print(f"{what}: {i}/{n}, {fm.calls} API calls, {time.time() - t0:.0f}s", flush=True)

    artists = listening.artist_hours(plays)
    for i, name in enumerate(artists, 1):
        fm.artist(name)
        progress("artists", i, len(artists))
    tracks = listening.tracks_for_lookup(plays)
    for i, (artist, track) in enumerate(tracks, 1):
        fm.track(artist, track)
        progress("tracks", i, len(tracks))
    names = [g["name"] for g in genres.load_enao()]
    for i, name in enumerate(names, 1):
        fm.tag_reach(name)
        progress("genre reach", i, len(names))


if __name__ == "__main__":
    if sys.argv[1:] == ["warm"]:
        warm()
    else:
        print(__doc__)
