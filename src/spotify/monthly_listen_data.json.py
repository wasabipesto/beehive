import json
import sys

import listening
from takeout import load_plays

json.dump(listening.monthly_listen_data(listening.recent(load_plays())), sys.stdout)
