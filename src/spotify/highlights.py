"""Highlighted artists and tracks for the spotify page, with cover art and previews.

Every track comes out as a "track item": track, album, Spotify URL, cover (300 px),
cover_small (64 px) and a 30-second preview URL, any of which can be None.
"""

import math
from collections import Counter, defaultdict
from datetime import datetime, timedelta

import listening
from lastfm import LastFM
from takeout import LOCAL_TZ, Play, name_key

RECENT_DAYS = 180
MIN_PLAY_MS = 30_000  # a play counts towards "instant favourites" if it lasted this long


def track_item(fm: LastFM, p: Play | None) -> dict:
    if p is None:
        return {"track": None, "album": None, "url": None, "cover": None, "cover_small": None, "preview": None}
    meta = fm.spotify_track(p.track_uri) if p.track_uri else {}
    cover = meta.get("cover")
    if not cover:  # a scrobbled track with no Spotify match: Last.fm's album art
        cover = (fm.track(p.artist, p.track) or {}).get("image")
    return {
        "track": p.track,
        "album": p.album,
        "url": f"https://open.spotify.com/track/{p.track_uri.rsplit(':', 1)[-1]}" if p.track_uri else None,
        "cover": cover,
        "cover_small": meta.get("cover_small") or cover,
        "preview": meta.get("preview"),
    }


def _top_track(plays: list[Play], artist: str, album: str | None = None) -> Play | None:
    """The artist's most-played track (optionally within one album); prefers a play with a URI."""
    ms, best = Counter(), {}
    for p in plays:
        if p.artist == artist and (album is None or p.album == album):
            ms[p.track_key] += p.ms_played
            if p.track_uri or p.track_key not in best:
                best[p.track_key] = p
    return best[ms.most_common(1)[0][0]] if ms else None


def _hours_by_artist(plays: list[Play]) -> Counter:
    h = Counter()
    for p in plays:
        h[p.artist] += p.ms_played / 3.6e6
    return h


def consistent(plays: list[Play], clusters: list[dict], fm: LastFM, n: int = 5) -> list[dict]:
    """From each of the top n clusters, the artist I've listened to most steadily.

    Steadiness is the sum over months of sqrt(hours), so ten steady months beat one huge one.
    """
    monthly = defaultdict(Counter)
    for p in plays:
        monthly[p.artist][p.month] += p.ms_played / 3.6e6
    steadiness = {a: sum(math.sqrt(h) for h in months.values()) for a, months in monthly.items()}
    out = []
    for c in clusters[:n]:
        artist = max(c["artists"], key=lambda a: steadiness.get(a, 0))
        out.append(
            {
                "artist": artist,
                "hours": round(sum(monthly[artist].values()), 1),
                "label": " / ".join(c["genres"]),
                "color": c["color"],
                **track_item(fm, _top_track(plays, artist)),
            }
        )
    return out


def recent(plays: list[Play], fm: LastFM, n: int = 8) -> dict:
    """The n artists I've played most in the last RECENT_DAYS days, with their top track then."""
    cutoff = plays[-1].ts - timedelta(days=RECENT_DAYS)
    window = [p for p in plays if p.ts >= cutoff]
    items = [
        {"artist": artist, "hours": round(hours, 1), **track_item(fm, _top_track(window, artist))}
        for artist, hours in _hours_by_artist(window).most_common(n)
    ]
    return {"since": cutoff.date().isoformat(), "items": items}


def quilt(plays: list[Play], clusters: list[dict], fm: LastFM, rows: int = 5) -> list[dict]:
    """One column per cluster: its top artists, each shown by their most-played album."""
    albums = defaultdict(Counter)
    for p in plays:
        if p.album:
            albums[p.artist][p.album] += p.ms_played
    hours = _hours_by_artist(plays)
    columns = []
    for c in clusters:
        tiles = []
        for artist in c["artists"][:rows]:
            album = albums[artist].most_common(1)[0][0] if albums[artist] else None
            item = track_item(fm, _top_track(plays, artist, album))
            tiles.append({"artist": artist, "hours": round(hours[artist], 1), **item, "album": album or item["album"]})
        columns.append({"label": " / ".join(c["genres"]), "color": c["color"], "tiles": tiles})
    return columns


def underrated(plays: list[Play], profiles: dict[str, dict], fm: LastFM, n: int = 15, cards: int = 5) -> dict:
    """Artists (2+ hours) and songs (10+ plays) I play a lot that few Last.fm users do."""
    artists = sorted(
        (p for p in profiles.values() if p["hours"] >= 2 and p["listeners"]),
        key=lambda p: p["listeners"],
    )[:n]
    artist_rows = [
        {"artist": p["name"], "genre": p["genre"], "listeners": p["listeners"], "hours": round(p["hours"], 1)} for p in artists
    ]
    for row in artist_rows[:cards]:
        row.update(track_item(fm, _top_track(plays, row["artist"])))

    latest = {}
    for p in plays:
        if p.track_uri or name_key(p.artist, p.track) not in latest:
            latest[name_key(p.artist, p.track)] = p
    songs = []
    for t in listening.track_stats(plays):
        if t["play_count"] < 10:
            continue
        listeners = (fm.track(t["artist"], t["title"]) or {}).get("listeners")
        if listeners:
            songs.append((listeners, t))
    songs.sort(key=lambda s: s[0])
    song_rows = [
        {
            "artist": t["artist"],
            "listeners": listeners,
            "plays": t["play_count"],
            **track_item(fm, latest[name_key(t["artist"], t["title"])]),
        }
        for listeners, t in songs[:n]
    ]
    return {"artists": artist_rows, "songs": song_rows}


def instant_favorites(plays: list[Play], fm: LastFM, min_plays: int = 4, window_days: int = 30) -> list[dict]:
    """For each month, the new track I played most in its first 30 days (at least min_plays).

    Tracks first heard in the last 30 days of the data are left out until their window closes.
    """
    start = datetime(2018, 7, 1, tzinfo=LOCAL_TZ)  # the history proper starts in July 2018
    end = plays[-1].ts
    first, counted, total, example = {}, Counter(), Counter(), {}
    for p in plays:
        key = name_key(p.artist, p.track)
        first.setdefault(key, p.ts)
        if p.track_uri or key not in example:
            example[key] = p
        if p.ms_played >= MIN_PLAY_MS:
            total[key] += 1
            if p.ts - first[key] <= timedelta(days=window_days):
                counted[key] += 1
    best = {}
    for key, n in counted.items():
        t0 = first[key]
        if n < min_plays or t0 < start or t0 > end - timedelta(days=window_days):
            continue
        month = t0.strftime("%Y-%m")
        if month not in best or (n, total[key]) > (counted[best[month]], total[best[month]]):
            best[month] = key
    return [
        {
            "month": month,
            "artist": example[key].artist,
            "plays_first_30d": counted[key],
            "plays_total": total[key],
            **track_item(fm, example[key]),
        }
        for month, key in sorted(best.items())
    ]
