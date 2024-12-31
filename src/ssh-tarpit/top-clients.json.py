import os
import re
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import geohash2
import socket

load_dotenv()
api_base = os.environ["PROMETHEUS_API_BASE"]


def get_data_inst(query):
    params = {"query": query}
    response = requests.get(f"{api_base}/query", params=params)
    try:
        data = response.json()["data"]["result"]
    except:
        print(response.text)
        raise Exception
    return data


def reverse_dns_lookup(ipv4):
    try:
        return socket.gethostbyaddr(ipv4)[0]
    except socket.herror:
        return None


data = get_data_inst(
    "sum(increase(endlessh_client_open_count[90d])) by (ip, country, geohash) > 10"
)
output = [
    {
        "ip": item["metric"]["ip"],
        "rdns": reverse_dns_lookup(item["metric"]["ip"]),
        "geohash": item["metric"]["geohash"],
        "lat": geohash2.decode(item["metric"]["geohash"])[0],
        "long": geohash2.decode(item["metric"]["geohash"])[1],
        "country": item["metric"]["country"],
        "count": round(float(item["value"][1])),
    }
    for item in data
]
output.sort(key=lambda x: x["count"], reverse=True)

print(json.dumps(output, indent=4))
