import json
import sys

import listening
from takeout import load_plays

json.dump(listening.artist_stats(listening.recent(load_plays())), sys.stdout)
