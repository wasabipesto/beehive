import json
import sys

import genres
import highlights
import listening
from lastfm import LastFM
from takeout import load_plays

plays = listening.recent(load_plays())
fm = LastFM()
json.dump(highlights.underrated(plays, genres.artist_profiles(plays, fm), fm), sys.stdout)
