import json
import sys

import highlights
from lastfm import LastFM
from takeout import load_plays

json.dump(highlights.instant_favorites(load_plays(), LastFM()), sys.stdout)
