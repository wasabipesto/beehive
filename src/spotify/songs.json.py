import json
import sys

import genres
import listening
from lastfm import LastFM
from takeout import load_plays

plays = listening.recent(load_plays())
profiles = genres.artist_profiles(plays)
finished = listening.track_durations(plays, finished_only=True)
longest = listening.track_durations(plays)
fm = LastFM()
out = []
for t in listening.track_stats(plays):
    info = fm.track(t["artist"], t["title"]) or {}
    p = profiles[t["artist"]]
    out.append(
        {
            "title": t["title"],
            "artist": t["artist"],
            "play_count": t["play_count"],
            "ms_played": t["ms_played"],
            # The longest play that ran to the end; else Last.fm's length; else the longest play.
            "duration_ms": finished.get(t["track_uri"]) or info.get("duration_ms") or longest.get(t["track_uri"]) or None,
            "listeners": info.get("listeners"),
            "genre": p["genre"],
            "genre_color": p["color"],
        }
    )
json.dump(out, sys.stdout)
