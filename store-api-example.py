"""
Apify Store API - Python quick-start example.

This API returns commercial intelligence on every public Actor in the Apify
Store: pricing, usage trends, reliability, ratings, and categories, as clean
structured JSON.

Actor landing page: https://apify.com/johnvc/store-actor-intelligence-api?fpr=9n7kx3
Get a free API key:  https://apify.com?fpr=9n7kx3

Run it:
    uv sync
    cp .env.example .env        # then paste your APIFY_API_TOKEN
    uv run python store-api-example.py
"""

import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("APIFY_API_TOKEN")
if not API_TOKEN:
    raise SystemExit(
        "Set APIFY_API_TOKEN in your environment or .env file. "
        "Get a free token at https://apify.com?fpr=9n7kx3"
    )

client = ApifyClient(API_TOKEN)

# Inputs are kept small (maxItems=10, enrichment off) to keep this first run
# inexpensive. Raise maxItems once you have your own API key and know your
# budget; set maxItems=0 to sweep the entire Store (~33,000+ Actors).
run_input = {
    "search": "instagram",          # keyword filter across title, name, description, developer
    "category": "SOCIAL_MEDIA",     # one of 25 Store categories; omit for all
    "pricingModel": "PAY_PER_EVENT",  # FREE, FLAT_PRICE_PER_MONTH, PRICE_PER_DATASET_ITEM, PAY_PER_EVENT
    "sortBy": "popularity",          # relevance, popularity, newest, lastUpdate
    "maxItems": 10,                  # cap the run small for the first try
    "includeDetails": False,         # set True to also pull each Actor's README + input schema
}

run = client.actor("johnvc/store-actor-intelligence-api").call(run_input=run_input)

if run is None:
    raise SystemExit("The Actor run did not return a result.")

# Read results from the run's default dataset. Each item is one Store Actor.
print("Top Apify Store Actors for this query:\n")
count = 0
for item in client.dataset(run.default_dataset_id).iterate_items():
    if item.get("result_type") != "actor":
        continue
    count += 1
    title = item.get("title")
    user = item.get("username")
    pricing = item.get("pricingModel")
    total_users = item.get("totalUsers")
    monthly = item.get("monthlyUsers")
    success = item.get("successRate30Days")
    rating = item.get("reviewRating")
    url = item.get("url")
    print(f"{count}. {title}  (by {user})")
    print(f"   pricing={pricing}  users={total_users}  monthly={monthly}  "
          f"success30d={success}%  rating={rating}")
    print(f"   {url}\n")

print(f"Returned {count} Actors. Raise maxItems (0 = entire Store) for more.")
