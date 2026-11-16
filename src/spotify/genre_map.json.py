import json
import sys

import genres
from lastfm import LastFM

# The ENAO genre map, with each genre's Last.fm reach (users who have used it as a tag),
# 0 where the genre isn't a Last.fm tag.
fm = LastFM()
out = [
    {"name": g["name"], **{f"{d}_norm": g[d] for d in genres.DIMS}, "color": g["color"], "reach": fm.tag_reach(g["name"])}
    for g in genres.load_enao()
]
json.dump(out, sys.stdout)
