import os
import re
import time
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
api_base = os.environ["PROMETHEUS_API_BASE"]


# takes range query and returns dict of {datestring: float}
def get_data_range(query):
    end = datetime.now()
    start = end - timedelta(days=365)  # look back 1 year
    step = timedelta(days=1)  # bucket width 1 day
    params = {
        "query": query,
        "start": start.timestamp(),
        "end": end.timestamp(),
        "step": step.total_seconds(),
    }

    response = requests.get(f"{api_base}/query_range", params=params)
    try:
        data = response.json()["data"]["result"]
    except:
        print(response.text)
        raise Exception

    flattened_data = {}
    for result in data:
        for value in result["values"]:
            timestamp = value[0]
            date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
            value = float(value[1])  # query must return a float value
            flattened_data[date] = value
    return flattened_data


dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(365)]
serieses = {
    "trapped_seconds_total": get_data_range(
        "increase(endlessh_trapped_time_seconds_total[1d])"
    ),
}

output = []
for date in dates:
    day_values = {"date": date}
    for series, values in serieses.items():
        day_values[series] = values[date]
    output.append(day_values)

print(json.dumps(output, indent=4))
