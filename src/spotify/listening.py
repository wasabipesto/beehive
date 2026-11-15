"""Aggregations over takeout plays, shared by the spotify data loaders.

Each function takes the list of takeout.Play objects and returns JSON-ready data.
"""

from collections import Counter, defaultdict
from datetime import datetime, time

from takeout import LOCAL_TZ, Play

# The 2012 plays are a handful of stray listens years before the history really starts.
HISTORY_START = datetime(2013, 1, 1, tzinfo=LOCAL_TZ)


def recent(plays: list[Play]) -> list[Play]:
    return [p for p in plays if p.ts >= HISTORY_START]


def by_month(plays: list[Play]) -> dict[str, list[Play]]:
    months = defaultdict(list)
    for p in plays:
        months[p.month].append(p)
    return dict(sorted(months.items()))


def track_durations(plays: list[Play]) -> dict[str, int]:
    """Estimate each track's length from the takeout alone.

    Uses the longest play that ran to the end of the track; tracks never finished fall
    back to their longest play, which underestimates them (so skips are undercounted).
    """
    finished, longest = {}, {}
    for p in plays:
        longest[p.track_uri] = max(longest.get(p.track_uri, 0), p.ms_played)
        if p.reason_end == "trackdone":
            finished[p.track_uri] = max(finished.get(p.track_uri, 0), p.ms_played)
    return {uri: finished.get(uri, ms) for uri, ms in longest.items()}


def monthly_summary(plays: list[Play]) -> list[dict]:
    out = []
    for month, listens in by_month(plays).items():
        top_track, _ = Counter((p.track, p.artist) for p in listens).most_common(1)[0]
        top_artist, _ = Counter(p.artist for p in listens).most_common(1)[0]
        out.append(
            {
                "month": month,
                "total_plays": len(listens),
                "total_skips": sum(p.skipped for p in listens),
                "total_listen_hours": round(sum(p.ms_played for p in listens) / 3.6e6, 2),
                "unique_tracks": len({p.track_uri for p in listens}),
                "top_track": f"{top_track[0]} by {top_track[1]}",
                "unique_artists": len({p.artist for p in listens}),
                "top_artist": top_artist,
            }
        )
    return sorted(out, key=lambda m: m["month"], reverse=True)


def _time_of_day(ts: datetime) -> str:
    t = ts.time()
    if time(4) <= t < time(12):
        return "Morning"
    if time(12) <= t < time(20):
        return "Afternoon"
    return "Night"


def monthly_listen_data(plays: list[Play]) -> list[dict]:
    """Monthly proportions, in the long format the page's stacked bar charts use."""
    durations = track_durations(plays)
    out = []

    def add(month, trend, shares):
        out.extend({"month": month, "trend": trend, "label": k, "value": round(v, 4)} for k, v in shares.items())

    for month, listens in by_month(plays).items():
        played = sum(p.ms_played for p in listens)
        unplayed = sum(max(0, durations[p.track_uri] - p.ms_played) for p in listens)
        add(month, "skipped", {"Skipped": unplayed / (unplayed + played), "Played": played / (unplayed + played)})
        shuffled = sum(p.ms_played for p in listens if p.shuffle)
        add(month, "shuffle", {"Shuffled": shuffled / played, "Not Shuffled": 1 - shuffled / played})
        tod = {"Morning": 0, "Afternoon": 0, "Night": 0}
        for p in listens:
            tod[_time_of_day(p.ts)] += p.ms_played
        add(month, "time_of_day", {k: v / played for k, v in tod.items()})
    return out


def discovered_monthly(plays: list[Play], min_plays: int = 3) -> list[dict]:
    """For each month, the new track played most on the day it was first heard."""
    first_day = {}
    for p in plays:
        first_day.setdefault(p.track_uri, p.ts.date())
    counts = defaultdict(Counter)
    meta = {}
    for p in plays:
        if p.ts.date() == first_day[p.track_uri]:
            counts[p.month][p.track_uri] += 1
            meta[p.track_uri] = (p.track, p.artist)
    out = []
    for month, c in sorted(counts.items(), reverse=True):
        uri, n = c.most_common(1)[0]
        if n >= min_plays:
            out.append({"month": month, "title": meta[uri][0], "artist": meta[uri][1], "plays": n})
    return out


def artist_stats(plays: list[Play]) -> list[dict]:
    """Per-artist totals. Artists are Spotify's album-artist names (the takeout has no IDs)."""
    stats = {}
    for p in plays:
        a = stats.setdefault(p.artist, {"name": p.artist, "play_count": 0, "skipped_count": 0, "ms_played": 0, "songs": set()})
        a["play_count"] += 1
        a["skipped_count"] += p.skipped
        a["ms_played"] += p.ms_played
        a["songs"].add(p.track_uri)
    out = [
        {k: v for k, v in a.items() if k != "songs"} | {"num_played_songs": len(a["songs"])}
        for a in stats.values()
    ]
    return sorted(out, key=lambda a: a["ms_played"], reverse=True)
