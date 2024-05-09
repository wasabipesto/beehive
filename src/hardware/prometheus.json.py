import os
import re
import time
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
api_base = os.environ["PROMETHEUS_API_BASE"]


def get_data(query):
    end = time.time()
    start = end - 6 * 30 * 24 * 60 * 60  # start is 6 months ago
    step = 60 * 60  # interval is 1 hour
    params = {
        "query": query,
        "start": start,
        "end": end,
        "step": step,
    }
    response = requests.get(f"{api_base}/query_range", params=params)
    try:
        data = response.json()["data"]["result"]
    except:
        print(response.text)
        raise Exception

    flattened_data = []
    for result in data:
        for value in result["values"]:
            instance = re.sub(r"\..*", "", result["metric"]["instance"])
            flattened_data.append(
                {
                    "time": value[0],
                    "value": value[1],
                    "instance": instance,
                }
            )

    return flattened_data


output = {
    # "memory_used_bytes": get_data("(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)"),
    "memory_used_pct": get_data(
        "(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemAvailable_bytes",
    ),
    "cpu_used_pct": get_data(
        'avg without (mode,cpu) (1 - rate(node_cpu_seconds_total{mode="idle"}[1m]))',
    ),
    "cloudflared_responses": get_data(
        "rate(cloudflared_tunnel_response_by_code[1m])",
    ),
}

print(json.dumps(output, indent=4))
