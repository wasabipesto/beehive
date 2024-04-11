import os
import json
import time
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from notion_client import Client
from notion_client.helpers import collect_paginated_api

load_dotenv()
notion = Client(auth=os.environ["NOTION_API_KEY"])

output_dir = "/opt/beehive/pages/assets-raw/media/posters"
timeout = 30

results = collect_paginated_api(
    notion.databases.query, database_id="588b7192cefe47588ab0166c8579f081"
)

items = [
    {
        "id": item["id"],
        "image_link": item["properties"]["Image Link"]["url"],
    }
    for item in results
    if item["properties"]["Image Link"]["url"]
]


def download_image(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            print(f"Rate limit exceeded. Sleeping for {timeout} seconds...")
            time.sleep(timeout)
            continue
        elif response.status_code != 200:
            # print(f"Error when trying to access {url}")
            # print(f"Server responded with code {response.status_code}")
            raise Exception
        return response


for i in items:
    file_path = os.path.join(output_dir, f'{i["id"]}.jpg')
    image_link = i["image_link"]
    if not os.path.exists(file_path):
        try:
            response = download_image(image_link)
            img = Image.open(BytesIO(response.content))
            if img.format != "JPEG":
                img = img.convert("RGB")
            img.save(file_path, "JPEG")
            print(f"Saved {image_link} to {file_path}")
        except:
            print(f"Failed to download {image_link}")
