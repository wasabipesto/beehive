import os
import json
import arrow
import requests
from dotenv import load_dotenv

load_dotenv()
api_base = os.environ["FEVER_API_BASE"]
api_data = {"api_key": os.environ["FEVER_API_KEY"]}
redact_patterns = ["rss-bridge", "kill-the-newsletter", "memberfulcontent", "mynews"]

group_response = requests.post(api_base + "&groups", data=api_data).json()
feed_response = requests.post(api_base + "&feeds", data=api_data).json()
favicon_response = requests.post(api_base + "&favicons", data=api_data).json()
# item_response = requests.post(api_base + "&items", data=api_data).json()

groups = {group["id"]: group for group in group_response["groups"]}
group_map = group_response["feeds_groups"]
favicons = {favicon["id"]: favicon["data"] for favicon in favicon_response["favicons"]}
feeds = {}
for feed in feed_response["feeds"]:
    for pattern in redact_patterns:
        if pattern in feed["url"]:
            feed["url"] = None
            break
    for pattern in redact_patterns:
        if pattern in feed["site_url"]:
            feed["site_url"] = None
            break
    feeds.update(
        {
            feed["id"]: {
                "title": feed["title"],
                "favicon": favicons[feed["favicon_id"]],
                "url": feed["url"],
                "site_url": feed["site_url"],
                "last_updated_humanized": arrow.get(
                    feed["last_updated_on_time"]
                ).humanize(),
            }
        }
    )

feeds_by_group = []
for gm in group_map:
    group = groups[gm["group_id"]]
    feed_ids = gm["feed_ids"].split(",")
    group_feeds = [feeds[int(feed_id)] for feed_id in feed_ids]
    feeds_by_group.append({"group": group, "feeds": group_feeds})

print(json.dumps(feeds_by_group, indent=4))
