"""Favourite artists and tracks, one per taste cluster, for the spotify page."""

import math
from collections import Counter, defaultdict
from datetime import timedelta

from lastfm import LastFM
from takeout import Play

RECENT_DAYS = 90


def _top_track(plays: list[Play], artist: str) -> Play | None:
    ms, last = Counter(), {}
    for p in plays:
        if p.artist == artist:
            ms[p.track_key] += p.ms_played
            last[p.track_key] = p
    return last[ms.most_common(1)[0][0]] if ms else None


def _card(fm: LastFM, cluster: dict, artist: str, hours: float, track: Play | None) -> dict:
    cover = fm.spotify_cover(track.track_uri) if track and track.track_uri else None
    if track and not cover:
        cover = (fm.track(track.artist, track.track) or {}).get("image")
    return {
        "cluster": " / ".join(cluster["genres"]),
        "color": cluster["color"],
        "artist": artist,
        "hours": round(hours, 1),
        "track": track.track if track else None,
        "track_uri": track.track_uri if track else None,
        "cover": cover,
    }


def favorites(plays: list[Play], clusters: list[dict], n_clusters: int = 5, fm: LastFM | None = None) -> dict:
    """One consistent and one recent favourite from each of the top clusters.

    Consistent = listening spread over many months: the sum over months of sqrt(hours),
    so ten steady months beat one huge one. Recent = most hours in the last 90 days.
    """
    fm = fm or LastFM()
    cutoff = plays[-1].ts - timedelta(days=RECENT_DAYS)
    recent_plays = [p for p in plays if p.ts >= cutoff]
    monthly = defaultdict(Counter)
    recent = Counter()
    for p in plays:
        monthly[p.artist][p.month] += p.ms_played / 3.6e6
    for p in recent_plays:
        recent[p.artist] += p.ms_played / 3.6e6
    steadiness = {a: sum(math.sqrt(h) for h in months.values()) for a, months in monthly.items()}

    out = {"consistent": [], "recent": [], "recent_since": cutoff.date().isoformat()}
    for c in clusters[:n_clusters]:
        steady = max(c["artists"], key=lambda a: steadiness.get(a, 0))
        out["consistent"].append(_card(fm, c, steady, sum(monthly[steady].values()), _top_track(plays, steady)))
        now = max(c["artists"], key=lambda a: recent.get(a, 0))
        if recent.get(now, 0) > 0:
            out["recent"].append(_card(fm, c, now, recent[now], _top_track(recent_plays, now)))
    return out
