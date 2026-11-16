import json
import sys

import favorites
import genres
import listening
from takeout import load_plays

plays = listening.recent(load_plays())
profiles = genres.artist_profiles(plays)
clusters = genres.clusters(profiles, k=8)
json.dump(
    {
        "clusters": [
            c | {"artists": [{"name": a, "hours": round(profiles[a]["hours"], 1)} for a in c["artists"][:10]], "artist_count": len(c["artists"])}
            for c in clusters
        ],
        "favorites": favorites.favorites(plays, clusters),
    },
    sys.stdout,
)
