import os
from dotenv import load_dotenv
import json
from notion_client import Client
from notion_client.helpers import collect_paginated_api

load_dotenv()
notion = Client(auth=os.environ["NOTION_API_KEY"])

results = collect_paginated_api(
    notion.databases.query, database_id="d1cf2e137fe44864bf4dcd5a7a4d1864"
)

software_by_category = {}
for item in results:
    category_obj = item["properties"]["Category"]
    if category_obj["select"]:
        category_id = category_obj["select"]["id"]
        category = category_obj["select"]["name"]
    else:
        continue

    name = item["properties"]["Name"]["title"][0]["text"]["content"]
    link = item["properties"]["URL"]["url"]

    description_obj = item["properties"]["Description"]
    if len(description_obj["rich_text"]):
        description = description_obj["rich_text"][0]["text"]["content"]
    else:
        description = None

    hosts = [i["name"] for i in item["properties"]["Hosts"]["multi_select"]]
    if len(hosts) == 0:
        continue

    notion_url = item["public_url"]

    if not category_id in software_by_category:
        software_by_category.update({category_id: {"name": category, "items": []}})

    software_by_category[category_id]["items"].append(
        {
            "name": name,
            "link": link,
            "description": description,
            "hosts": hosts,
            "notion_url": notion_url,
        }
    )

software_by_category = dict(
    sorted(software_by_category.items(), key=lambda x: x[1]["name"])
)
print(json.dumps(software_by_category, indent=4))
