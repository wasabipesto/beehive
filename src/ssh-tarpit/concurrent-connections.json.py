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
    10: get_data_range(
        "quantile_over_time(0.10, (endlessh_client_open_count_total - endlessh_client_closed_count_total)[1d:1m])"
    ),
    25: get_data_range(
        "quantile_over_time(0.25, (endlessh_client_open_count_total - endlessh_client_closed_count_total)[1d:1m])"
    ),
    50: get_data_range(
        "quantile_over_time(0.50, (endlessh_client_open_count_total - endlessh_client_closed_count_total)[1d:1m])"
    ),
    75: get_data_range(
        "quantile_over_time(0.75, (endlessh_client_open_count_total - endlessh_client_closed_count_total)[1d:1m])"
    ),
    90: get_data_range(
        "quantile_over_time(0.90, (endlessh_client_open_count_total - endlessh_client_closed_count_total)[1d:1m])"
    ),
    95: get_data_range(
        "quantile_over_time(0.95, (endlessh_client_open_count_total - endlessh_client_closed_count_total)[1d:1m])"
    ),
    99: get_data_range(
        "quantile_over_time(0.99, (endlessh_client_open_count_total - endlessh_client_closed_count_total)[1d:1m])"
    ),
}

output = []
for date in dates:
    for series, values in serieses.items():
        day_values = {
            "date": date,
            "value": values[date],
            "percentile": series,
        }
        output.append(day_values)

print(json.dumps(output, indent=4))
