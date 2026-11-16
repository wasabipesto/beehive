"""Load the full listening history as a list of plays.

Shared by the spotify data loaders. Three sources are layered, each used only after the
previous one ends, so nothing is counted twice:

1. Spotify "Extended streaming history" (Streaming_History_Audio*.json): the full record,
   with track IDs, skips and shuffle. Requested once a year or so.
2. Spotify "Account data" (StreamingHistory_music_*.json): the past year, artist/track
   names and play time only. Quicker to request, so it bridges the gap after (1).
3. Last.fm scrobbles: everything since, fetched on each build.

Put the export zips (or their extracted folders) in SPOTIFY_TAKEOUT_DIR. Only the fields
the page needs are kept; the exports also carry IP addresses and countries, which never
leave this module.
"""

import io
import json
import os
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

# Local time for "time of day" and month bucketing.
LOCAL_TZ = ZoneInfo("America/New_York")
# A scrobble doesn't say how long it played; assume the whole track, or this if unknown.
DEFAULT_TRACK_MS = 210_000


@dataclass(frozen=True, slots=True)
class Play:
    ts: datetime  # local time (LOCAL_TZ) the play ended
    track: str
    artist: str  # album artist, as Spotify reports it
    album: str | None
    ms_played: int
    source: str  # "extended", "account" or "scrobble"
    track_uri: str | None = None  # Spotify URI, when known
    shuffle: bool | None = None  # only in the extended history
    skipped: bool | None = None
    reason_start: str | None = None
    reason_end: str | None = None

    @property
    def track_key(self) -> str:
        return self.track_uri or name_key(self.artist, self.track)

    @property
    def month(self) -> str:
        return self.ts.strftime("%Y-%m")


def name_key(artist: str, track: str) -> str:
    return f"{artist.casefold().strip()}\x1f{track.casefold().strip()}"


def _files(root: Path, prefix: str):
    """Yield the bytes of every <prefix>*.json under root, zipped or not."""
    for path in sorted(root.rglob("*")):
        if path.suffix == ".zip":
            with zipfile.ZipFile(path) as z:
                for name in sorted(z.namelist()):
                    if Path(name).name.startswith(prefix) and name.endswith(".json"):
                        yield z.read(name)
        elif path.name.startswith(prefix) and path.suffix == ".json":
            yield path.read_bytes()


def _extended(root: Path) -> list[Play]:
    seen, plays = set(), []
    for raw in _files(root, "Streaming_History_Audio"):
        for r in json.load(io.BytesIO(raw)):
            uri = r.get("spotify_track_uri")
            if not uri or not r.get("master_metadata_track_name"):
                continue  # podcasts, audiobooks
            # The export repeats some rows byte for byte, and overlapping exports repeat more.
            key = (r["ts"], uri, r["ms_played"])
            if key in seen:
                continue
            seen.add(key)
            plays.append(
                Play(
                    ts=datetime.fromisoformat(r["ts"].replace("Z", "+00:00")).astimezone(LOCAL_TZ),
                    track=r["master_metadata_track_name"],
                    artist=r["master_metadata_album_artist_name"],
                    album=r["master_metadata_album_album_name"],
                    ms_played=r["ms_played"],
                    source="extended",
                    track_uri=uri,
                    shuffle=bool(r.get("shuffle")),
                    skipped=bool(r.get("skipped")),
                    reason_start=r.get("reason_start") or "",
                    reason_end=r.get("reason_end") or "",
                )
            )
    return plays


def _account(root: Path) -> list[Play]:
    seen, plays = set(), []
    for raw in _files(root, "StreamingHistory_music"):
        for r in json.load(io.BytesIO(raw)):
            key = (r["endTime"], r["artistName"], r["trackName"], r["msPlayed"])
            if key in seen:
                continue
            seen.add(key)
            ts = datetime.strptime(r["endTime"], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
            plays.append(Play(ts.astimezone(LOCAL_TZ), r["trackName"], r["artistName"], None, r["msPlayed"], "account"))
    return plays


def _scrobbles(since: datetime, durations: dict[str, int]) -> list[Play]:
    if not os.environ.get("LASTFM_USERNAME"):
        return []
    from lastfm import LastFM  # only needed when scrobbles are configured

    fm = LastFM()
    fm.sync_scrobbles(os.environ["LASTFM_USERNAME"])
    plays = []
    for uts, artist, track, album in fm.scrobbles(since=int(since.timestamp())):
        ms = durations.get(name_key(artist, track), DEFAULT_TRACK_MS)
        # Last.fm stamps the start of the track; Spotify stamps the end.
        ts = datetime.fromtimestamp(uts + ms / 1000, timezone.utc).astimezone(LOCAL_TZ)
        if ts > since:
            plays.append(Play(ts, track, artist, album or None, ms, "scrobble"))
    return plays


def load_plays(root: str | os.PathLike | None = None, scrobbles: bool = True) -> list[Play]:
    """All music plays, oldest first, from every source in SPOTIFY_TAKEOUT_DIR plus Last.fm."""
    root = Path(root or os.environ["SPOTIFY_TAKEOUT_DIR"]).expanduser()
    plays = _extended(root)
    if not plays:
        raise SystemExit(f"no extended streaming history found under {root}")
    end = max(p.ts for p in plays)
    plays += [p for p in _account(root) if p.ts > end]
    end = max(p.ts for p in plays)

    # Spotify URIs and track lengths from the extended history, matched by name, so later
    # plays of a known track get its URI and scrobbles get a play time.
    uris, durations = {}, {}
    for p in plays:
        if p.source == "extended":
            k = name_key(p.artist, p.track)
            uris[k] = p.track_uri
            if p.reason_end == "trackdone":
                durations[k] = max(durations.get(k, 0), p.ms_played)
    if scrobbles:
        plays += _scrobbles(end, durations)
    plays = [p if p.track_uri else _with_uri(p, uris.get(name_key(p.artist, p.track))) for p in plays]
    plays.sort(key=lambda p: p.ts)
    return plays


def _with_uri(p: Play, uri: str | None) -> Play:
    if uri is None:
        return p
    return Play(p.ts, p.track, p.artist, p.album, p.ms_played, p.source, uri)
