import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ["FRED_API_KEY"]

response = requests.get(
    "https://api.stlouisfed.org/fred/series/observations",
    params={
        "series_id": "CPIAUCSL",
        "api_key": api_key,
        "file_type": "json",
        "observation_start": "2000-01-01",
        "frequency": "m",
        "aggregation_method": "eop",
    },
).json()

output = [
    {"date": item["date"], "value": float(item["value"])}
    for item in response["observations"]
]

for i, item in enumerate(output):
    if i > 0:
        item["delta"] = item["value"] - output[i - 1]["value"]

print(json.dumps(output, indent=4))
