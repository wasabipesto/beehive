import os
import numpy as np
import json
import arrow
import requests
from dotenv import load_dotenv

load_dotenv()
api_base = os.environ["TAUTULLI_API_BASE"]
apikey = os.environ["TAUTULLI_API_KEY"]

hardcoded_sizes = {"total_available_kb": 46687416728, "parity_kb": 12884901888}

plays_per_month = requests.get(
    api_base,
    params={
        "apikey": apikey,
        "cmd": "get_plays_per_month",
        "y_axis": "duration",
        "time_range": 60,
    },
).json()
ppm = plays_per_month["response"]["data"]
plays_history = []
for series in ppm["series"]:
    for i in range(len(plays_per_month["response"]["data"]["categories"])):
        date = arrow.get(ppm["categories"][i], "MMM YYYY")
        plays_history.append(
            {
                "month": date.format("YYYY-MM"),
                "library": series["name"],
                "hours": series["data"][i] / 3600,
            }
        )
plays_history_summary = {
    "avg_hours_movies": int(
        round(
            np.mean([i["hours"] for i in plays_history if i["library"] == "Movies"]), -1
        )
    ),
    "avg_hours_tv": int(
        round(np.mean([i["hours"] for i in plays_history if i["library"] == "TV"]), -1)
    ),
}

home_stats = requests.get(
    api_base,
    params={
        "apikey": apikey,
        "cmd": "get_home_stats",
        "time_range": 30,
        "stats_type": "plays",
    },
).json()
home_stats_keyed = {i["stat_id"]: i for i in home_stats["response"]["data"]}
top_movies = home_stats_keyed["top_movies"]
popular_movies = home_stats_keyed["popular_movies"]
top_tv = home_stats_keyed["top_tv"]
popular_tv = home_stats_keyed["popular_tv"]

libraries_table = requests.get(
    api_base,
    params={"apikey": apikey, "cmd": "get_libraries_table"},
).json()
libraries_table_keyed = {
    i["section_name"]: i for i in libraries_table["response"]["data"]["data"]
}
library_movies = libraries_table_keyed["Movies"]
library_tv = libraries_table_keyed["TV Shows"]

library_media_info_movies = requests.get(
    api_base,
    params={
        "apikey": apikey,
        "cmd": "get_library_media_info",
        "section_id": library_movies["section_id"],
        "length": 999999,
    },
).json()
library_movies_items = [
    {
        "title": item["title"],
        "added_at": item["added_at"],
        "year": item["year"],
        "bitrate": item["bitrate"],
        "video_codec": item["video_codec"],
        "video_resolution": item["video_resolution"],
        "file_size": item["file_size"],
        "last_played": item["last_played"],
        "play_count": item["play_count"],
    }
    for item in library_media_info_movies["response"]["data"]["data"]
]

library_media_info_tv = requests.get(
    api_base,
    params={
        "apikey": apikey,
        "cmd": "get_library_media_info",
        "section_id": library_tv["section_id"],
        "length": 999999,
    },
).json()
library_tv_items = [
    {
        "title": item["title"],
        "added_at": item["added_at"],
        "year": item["year"],
        "bitrate": item["bitrate"],
        "video_codec": item["video_codec"],
        "video_resolution": item["video_resolution"],
        "file_size": item["file_size"],
        "last_played": item["last_played"],
        "play_count": item["play_count"],
    }
    for item in library_media_info_tv["response"]["data"]["data"]
]

output = {
    "plays_history": plays_history,
    "plays_history_summary": plays_history_summary,
    "popular_movies": popular_movies,
    "popular_tv": popular_tv,
    "hardcoded_sizes": hardcoded_sizes,
    "library_movies": library_movies,
    "library_tv": library_tv,
    "library_movies_items": library_movies_items,
    # "library_tv_items": library_tv_items,
}

print(json.dumps(output, indent=4))
# print(json.dumps(plays_per_month, indent=4))
