import requests

# Socrata open data sources — no API key required for public datasets.
# Find more animal shelter datasets at https://dev.socrata.com/data/
SOURCES = [
    {
        "city": "Austin",
        "state": "TX",
        "intakes_url": "https://data.austintexas.gov/resource/9t4d-g238.json",
        "outcomes_url": "https://data.austintexas.gov/resource/u3f4-9qnu.json",
    },
    # Add more cities by appending entries here, e.g.:
    # {
    #     "city": "Seattle",
    #     "state": "WA",
    #     "intakes_url": "https://data.seattle.gov/resource/<dataset_id>.json",
    #     "outcomes_url": "https://data.seattle.gov/resource/<dataset_id>.json",
    # },
]

PAGE_SIZE = 1000


def fetch_socrata(url: str) -> list[dict]:
    """Paginate through a Socrata endpoint and return all records."""
    records = []
    offset = 0
    domain = url.split("/")[2]

    while True:
        response = requests.get(
            url,
            params={"$limit": PAGE_SIZE, "$offset": offset, "$order": ":id"},
            timeout=30,
        )
        response.raise_for_status()
        batch = response.json()
        if not batch:
            break
        records.extend(batch)
        print(f"  {domain}: {len(records)} records fetched...")
        if len(batch) < PAGE_SIZE:
            break
        offset += PAGE_SIZE

    return records


def extract() -> dict[str, list[dict]]:
    """Fetch intakes and outcomes from all configured sources."""
    all_intakes = []
    all_outcomes = []

    for source in SOURCES:
        city, state = source["city"], source["state"]

        print(f"\n[{city}, {state}] Fetching intakes...")
        intakes = fetch_socrata(source["intakes_url"])
        for r in intakes:
            r["_source_city"] = city
            r["_source_state"] = state
        all_intakes.extend(intakes)

        print(f"[{city}, {state}] Fetching outcomes...")
        outcomes = fetch_socrata(source["outcomes_url"])
        for r in outcomes:
            r["_source_city"] = city
            r["_source_state"] = state
        all_outcomes.extend(outcomes)

    print(f"\nExtract complete: {len(all_intakes)} intakes, {len(all_outcomes)} outcomes")
    return {"intakes": all_intakes, "outcomes": all_outcomes}
