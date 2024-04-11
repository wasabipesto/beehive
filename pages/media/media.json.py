import os
import json
from dotenv import load_dotenv
from notion_client import Client
from notion_client.helpers import collect_paginated_api

load_dotenv()
notion = Client(auth=os.environ["NOTION_API_KEY"])

results = collect_paginated_api(
    notion.databases.query, database_id="588b7192cefe47588ab0166c8579f081"
)

items = [
    {
        "id": item["id"],
        "type": (
            item["properties"]["Type"]["select"]["name"]
            if item["properties"]["Type"].get("select")
            else None
        ),
        "title": (
            item["properties"]["Title"]["title"][0]["text"]["content"]
            if item["properties"]["Title"]["title"]
            else None
        ),
        "artist": (
            item["properties"]["Artist/Developer"]["rich_text"][0]["text"]["content"]
            if item["properties"]["Artist/Developer"]["rich_text"]
            else None
        ),
        "date": (
            item["properties"]["Date"]["date"]["start"]
            if item["properties"]["Date"]["date"]
            else None
        ),
        "medium": item["properties"]["Medium"]["number"],
        "effect": item["properties"]["Effect"]["number"],
        "enjoyability": item["properties"]["Enjoyability"]["number"],
        "story": item["properties"]["Story"]["number"],
        "tone": item["properties"]["Tone"]["number"],
        "average": item["properties"]["Average Rating"]["formula"]["number"],
        "media_link": item["properties"]["Media Link"]["url"],
        "image_link": item["properties"]["Image Link"]["url"],
        "notion_url": item["public_url"],
    }
    for item in results
]

items = [i for i in items if i["title"] and i["type"] and i["average"]]
items = sorted(items, key=lambda i: i["title"])

for item in items:
    if item["type"].endswith("s") or item["type"] == "Other":
        item.update({"category_name": item["type"]})
    else:
        item.update({"category_name": item["type"] + "s"})

top_items = [i for i in items if i["average"] >= 4]
categories = sorted(set(i["category_name"] for i in top_items))

output = {
    "categorized": [
        {
            "category_name": category,
            "items": [i for i in top_items if i["category_name"] == category],
        }
        for category in categories
    ],
    "all": items,
}

print(json.dumps(output, indent=4))
