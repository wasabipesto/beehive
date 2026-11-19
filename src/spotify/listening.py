"""Aggregations over takeout plays, shared by the spotify data loaders.

Each function takes the list of takeout.Play objects and returns JSON-ready data.
"""

from collections import Counter, defaultdict
from datetime import datetime, time

from takeout import LOCAL_TZ, Play, name_key

# The 2012 plays are a handful of stray listens years before the history really starts.
HISTORY_START = datetime(2013, 1, 1, tzinfo=LOCAL_TZ)


def recent(plays: list[Play]) -> list[Play]:
    return [p for p in plays if p.ts >= HISTORY_START]


def by_month(plays: list[Play]) -> dict[str, list[Play]]:
    months = defaultdict(list)
    for p in plays:
        months[p.month].append(p)
    return dict(sorted(months.items()))


def track_durations(plays: list[Play], finished_only: bool = False) -> dict[str, int]:
    """Estimate each track's length from the takeout alone.

    Uses the longest play that ran to the end of the track; tracks never finished fall
    back to their longest play, which underestimates them (so skips are undercounted).
    """
    finished, longest = {}, {}
    for p in plays:
        if p.source != "extended":
            continue
        longest[p.track_uri] = max(longest.get(p.track_uri, 0), p.ms_played)
        if p.reason_end == "trackdone":
            finished[p.track_uri] = max(finished.get(p.track_uri, 0), p.ms_played)
    if finished_only:
        return finished
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
                "total_skips": sum(bool(p.skipped) for p in listens),
                "total_listen_hours": round(sum(p.ms_played for p in listens) / 3.6e6, 2),
                "unique_tracks": len({p.track_key for p in listens}),
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
        # Skips and shuffle are only recorded in the extended history, so these shares come
        # from its plays alone (in a month it only partly covers, from that part).
        ext = [p for p in listens if p.source == "extended"]
        ext_played = sum(p.ms_played for p in ext)
        if ext_played:
            unplayed = sum(max(0, durations[p.track_uri] - p.ms_played) for p in ext)
            add(month, "skipped", {"Skipped": unplayed / (unplayed + ext_played), "Played": ext_played / (unplayed + ext_played)})
            shuffled = sum(p.ms_played for p in ext if p.shuffle)
            add(month, "shuffle", {"Shuffled": shuffled / ext_played, "Not Shuffled": 1 - shuffled / ext_played})
        tod = {"Morning": 0, "Afternoon": 0, "Night": 0}
        for p in listens:
            tod[_time_of_day(p.ts)] += p.ms_played
        add(month, "time_of_day", {k: v / played for k, v in tod.items()})
    return out


def artist_stats(plays: list[Play]) -> list[dict]:
    """Per-artist totals. Artists are Spotify's album-artist names (the takeout has no IDs)."""
    stats = {}
    for p in plays:
        a = stats.setdefault(p.artist, {"name": p.artist, "play_count": 0, "skipped_count": 0, "ms_played": 0, "songs": set()})
        a["play_count"] += 1
        a["skipped_count"] += bool(p.skipped)
        a["ms_played"] += p.ms_played
        a["songs"].add(p.track_key)
    out = [
        {k: v for k, v in a.items() if k != "songs"} | {"num_played_songs": len(a["songs"])}
        for a in stats.values()
    ]
    return sorted(out, key=lambda a: a["ms_played"], reverse=True)


def artist_hours(plays: list[Play]) -> list[str]:
    """Artist names, most-played first."""
    ms = Counter()
    for p in plays:
        ms[p.artist] += p.ms_played
    return [a for a, _ in ms.most_common()]


def tracks_for_lookup(plays: list[Play], min_hours: float = 0.5) -> list[tuple[str, str]]:
    """(artist, track) for every track the songs loader shows, most-played first."""
    return [(t["artist"], t["title"]) for t in track_stats(plays, min_hours)]


def track_stats(plays: list[Play], min_hours: float = 0.5) -> list[dict]:
    """Per-track totals for every track played at least min_hours, most-played first.

    Grouped by artist and title, so a song's single and album releases count as one.
    """
    stats = {}
    for p in plays:
        t = stats.setdefault(name_key(p.artist, p.track), {"title": p.track, "artist": p.artist, "track_uri": p.track_uri, "play_count": 0, "ms_played": 0})
        t["play_count"] += 1
        t["ms_played"] += p.ms_played
    out = [t for t in stats.values() if t["ms_played"] >= min_hours * 3.6e6]
    return sorted(out, key=lambda t: -t["ms_played"])
