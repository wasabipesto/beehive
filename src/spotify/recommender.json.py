import json
import sys
from collections import defaultdict

import genres
import highlights
import listening
from lastfm import LastFM
from takeout import load_plays

# A reverse similar-artist index: for each artist Last.fm lists as similar to one of mine
# (anyone I've played for MIN_HOURS), which of mine and how similar. The page looks an
# artist up here and suggests the closest of mine, favouring ones near the centre of my
# listening. My own artists are included, so they can be looked up too.
MIN_HOURS = 1.0

plays = listening.recent(load_plays())
fm = LastFM()
profiles = genres.artist_profiles(plays, fm)
mine = sorted((p for p in profiles.values() if p["hours"] >= MIN_HOURS and p["x"] is not None), key=lambda p: -p["hours"])
index_of = {p["name"]: i for i, p in enumerate(mine)}
by_lastfm = {p["lastfm_name"].casefold(): i for i, p in enumerate(mine) if p["lastfm_name"]}

names, entries = [], []
slot = {}  # casefolded candidate name -> position in names


def add(name, my_index, match):
    key = name.casefold()
    if key not in slot:
        slot[key] = len(names)
        names.append(name)
        entries.append({})
    links = entries[slot[key]]
    links[my_index] = max(links.get(my_index, 0), match)


for i, p in enumerate(mine):
    add(p["lastfm_name"] or p["name"], i, 1.0)  # so my own artists can be looked up
    for sim, match in (fm.artist(p["name"]) or {}).get("similar", []):
        add(sim, i, match)
        j = by_lastfm.get(sim.casefold())
        if j is not None:  # similarity runs both ways between two of mine
            add(mine[j]["lastfm_name"] or mine[j]["name"], i, match)

# Spotify's spelling of my artists ("STRFKR") as another name for Last.fm's ("Starfucker").
aliases = [
    [p["name"], slot[p["lastfm_name"].casefold()]]
    for p in mine
    if p["lastfm_name"] and p["name"].casefold() != p["lastfm_name"].casefold()
]
hours_total = sum(p["hours"] for p in mine)
out = {
    "center": {d: round(sum(p[d] * p["hours"] for p in mine) / hours_total, 2) for d in ("x", "y")},
    "mine": [
        {
            "artist": p["name"],
            "lastfm_name": p["lastfm_name"],
            "hours": round(p["hours"], 1),
            "genre": p["genre"],
            "color": p["color"],
            "x": p["x"],
            "y": p["y"],
            **highlights.track_item(fm, highlights._top_track(plays, p["name"])),
        }
        for p in mine
    ],
    "names": names,
    "aliases": aliases,  # [name, index into names]
    # Parallel to names: [my artist index, similarity as a percentage] pairs.
    "links": [[[i, round(m * 100)] for i, m in sorted(links.items(), key=lambda kv: -kv[1])] for links in entries],
}
json.dump(out, sys.stdout, ensure_ascii=False, separators=(",", ":"))
