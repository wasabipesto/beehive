import json
import sys

import genres
import listening
from takeout import load_plays

plays = listening.recent(load_plays())
profiles = genres.artist_profiles(plays)
out = []
for a in listening.artist_stats(plays):
    p = profiles[a["name"]]
    out.append(a | {"listeners": p["listeners"], "genre": p["genre"], "genre_color": p["color"], "x": p["x"], "y": p["y"]})
json.dump(out, sys.stdout)
