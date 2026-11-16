import json
import sys

import genres
import listening
from takeout import load_plays

plays = listening.recent(load_plays())
json.dump(genres.genre_totals(plays, genres.artist_profiles(plays), 75), sys.stdout)
