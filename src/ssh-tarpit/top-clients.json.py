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

CACHE_FILE = "src/ssh-tarpit/reverse_dns_cache.json"


# Load cache from disk
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}


# Save cache to disk
def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)


# Perform reverse DNS lookup with caching
def reverse_dns_lookup(ipv4, cache):
    if ipv4 in cache:
        return cache[ipv4]
    try:
        hostname = socket.gethostbyaddr(ipv4)[0]
    except socket.herror:
        hostname = None
    cache[ipv4] = hostname
    return hostname


# Get data from Prometheus API
def get_data_inst(query):
    params = {"query": query}
    response = requests.get(f"{api_base}/query", params=params)
    try:
        data = response.json()["data"]["result"]
    except:
        print(response.text)
        raise Exception("Error fetching data from Prometheus API")
    return data


# Load the cache
cache = load_cache()

# Query Prometheus API
data = get_data_inst(
    "sum(increase(endlessh_client_open_count[90d])) by (ip, country, geohash) >= 10"
)

# Process the data
output = []
for item in data:
    ip = item["metric"]["ip"]
    rdns = reverse_dns_lookup(ip, cache)
    geohash = item["metric"]["geohash"]
    lat, long = geohash2.decode(geohash)
    output.append(
        {
            "ip": ip,
            "rdns": rdns,
            "geohash": geohash,
            "lat": lat,
            "long": long,
            "country": item["metric"]["country"],
            "count": round(float(item["value"][1])),
        }
    )

# Save the updated cache
save_cache(cache)

# Sort the output by count and print
output.sort(key=lambda x: x["count"], reverse=True)
print(json.dumps(output, indent=4))
