import os
import json
from dotenv import load_dotenv
from notion_client import Client
from notion_client.helpers import collect_paginated_api

load_dotenv()
notion = Client(auth=os.environ["NOTION_API_KEY"])

results = collect_paginated_api(
    notion.databases.query, database_id="d1cf2e137fe44864bf4dcd5a7a4d1864"
)

software_items = [
    {
        "name": (
            item["properties"]["Name"]["title"][0]["text"]["content"]
            if item["properties"]["Name"]["title"]
            else None
        ),
        "emoji": item["icon"]["emoji"] if item.get("icon") else None,
        "category": (
            item["properties"]["Category"]["select"]["name"]
            if item["properties"]["Category"].get("select")
            else None
        ),
        "link": item["properties"]["URL"]["url"],
        "description": (
            item["properties"]["Description"]["rich_text"][0]["text"]["content"]
            if item["properties"]["Description"]["rich_text"]
            else None
        ),
        "hosts": [i["name"] for i in item["properties"]["Hosts"]["multi_select"]],
        "notion_url": item["public_url"],
    }
    for item in results
]

software_items = sorted(software_items, key=lambda i: i["name"])
categories = sorted(
    set(item["category"] for item in software_items if item["category"])
)

output = [
    {
        "category_name": category,
        "items": [
            item
            for item in software_items
            if item["category"] == category and not "Retired" in item["hosts"]
        ],
    }
    for category in categories
]

print(json.dumps(output, indent=4))
