import json
import sys

import genres
import listening
from takeout import load_plays

plays = listening.recent(load_plays())
profiles = genres.artist_profiles(plays)
out = {}
for month, listens in listening.by_month(plays).items():
    top = genres.genre_totals(listens, profiles, 25)
    hours = sum(g["hours_played"] for g in top)
    if not hours:
        continue
    out[month] = {
        "month": month,
        "top_genres": top,
        **{f"centroid_{d}": round(sum(g[f"{d}_norm"] * g["hours_played"] for g in top) / hours, 1) for d in genres.DIMS},
    }
json.dump(out, sys.stdout)
