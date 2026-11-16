"""Snapshot the genre map from Every Noise at Once into enao_genres.json.

Glenn McDonald's map (https://everynoise.com) places ~6,300 genres in two acoustic
dimensions (left = denser and atmospheric, right = spikier and bouncier; down = organic,
up = mechanical and electric) and colours them by energy (red), dynamic variation (green)
and instrumentalness (blue). It has been frozen since Spotify ended the project in 2023, so
this only needs re-running if the page ever changes:
    uv run src/spotify/enao_snapshot.py [saved-page.html]

Coordinates and colour channels are min-max scaled to 0-100, as in the original notebook.
"""

import html as htmllib
import json
import re
import sys
import urllib.request
from pathlib import Path

# The site sits behind a bot check that turns away non-browser user agents.
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
GENRE = re.compile(
    r'class="genre scanme"[^>]*?style="color: (#[0-9a-f]{6}); top: (\d+)px; left: (\d+)px; font-size: \d+%"[^>]*>([^<]*)'
)


def main():
    if len(sys.argv) > 1:
        html = Path(sys.argv[1]).read_text(encoding="utf-8")
    else:
        req = urllib.request.Request("https://everynoise.com/", headers={"User-Agent": UA})
        html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
    genres = []
    for color, top, left, name in GENRE.findall(html):
        genres.append(
            {
                "name": htmllib.unescape(name).replace("» ", "").strip(),
                "x": int(left),
                "y": -int(top),  # page coordinates grow downward
                "r": int(color[1:3], 16),
                "g": int(color[3:5], 16),
                "b": int(color[5:7], 16),
                "color": color,
            }
        )
    if len(genres) < 5000:
        raise SystemExit(f"only found {len(genres)} genres; the page layout may have changed")
    for k in ("x", "y", "r", "g", "b"):
        lo, hi = min(g[k] for g in genres), max(g[k] for g in genres)
        for g in genres:
            g[k] = round((g[k] - lo) / (hi - lo) * 100, 2)
    genres.sort(key=lambda g: g["name"])
    out = Path(__file__).with_name("enao_genres.json")
    out.write_text(json.dumps(genres, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"wrote {len(genres)} genres to {out}")


if __name__ == "__main__":
    main()
