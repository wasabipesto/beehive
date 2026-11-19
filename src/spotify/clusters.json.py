import json
import sys

import genres
import highlights
import listening
from lastfm import LastFM
from takeout import load_plays

plays = listening.recent(load_plays())
fm = LastFM()
profiles = genres.artist_profiles(plays, fm)
clusters = genres.clusters(profiles, k=8)
json.dump(
    {
        "clusters": [
            c | {"artists": [{"name": a, "hours": round(profiles[a]["hours"], 1)} for a in c["artists"][:10]], "artist_count": len(c["artists"])}
            for c in clusters
        ],
        "consistent": highlights.consistent(plays, clusters, fm),
        "recent": highlights.recent(plays, fm),
        "quilt": highlights.quilt(plays, clusters, fm),
    },
    sys.stdout,
)
