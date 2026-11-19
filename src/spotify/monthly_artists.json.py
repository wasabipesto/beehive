import json
import sys
from collections import Counter, defaultdict

import genres
import listening
from takeout import load_plays

# For each month, every artist I played, with their place on the genre map. There's no
# minimum: much of my listening is a few minutes each across a hundred-odd artists, and
# leaving those out hid most of some months. Artists are listed once and referenced by
# index to keep the file small.

plays = listening.recent(load_plays())
profiles = genres.artist_profiles(plays)
monthly = defaultdict(Counter)
for p in plays:
    monthly[p.month][p.artist] += p.ms_played / 3.6e6

artists, index, months = [], {}, []
for month in sorted(monthly):
    points = []
    for name, hours in monthly[month].most_common():
        prof = profiles[name]
        if hours <= 0 or prof["x"] is None:
            continue
        if name not in index:
            index[name] = len(artists)
            artists.append({"name": name, "x": prof["x"], "y": prof["y"], "genre": prof["genre"], "color": prof["color"]})
        points.append([index[name], round(hours, 3)])
    total = sum(monthly[month].values())
    placed = sum(h for _, h in points)
    months.append({"month": month, "hours": round(total, 1), "placed_hours": round(placed, 1), "points": points})
json.dump({"artists": artists, "months": months}, sys.stdout, separators=(",", ":"))
