import os
import requests
from dotenv import load_dotenv

load_dotenv()

PETFINDER_API_KEY = os.getenv("PETFINDER_API_KEY")
PETFINDER_SECRET = os.getenv("PETFINDER_SECRET")
BASE_URL = "https://api.petfinder.com/v2"


def get_access_token() -> str:
    response = requests.post(
        f"{BASE_URL}/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": PETFINDER_API_KEY,
            "client_secret": PETFINDER_SECRET,
        },
    )
    response.raise_for_status()
    return response.json()["access_token"]


def fetch_animals(animal_type: str, pages: int = 3) -> list[dict]:
    """Fetch dog or cat listings from the Petfinder API."""
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    animals = []

    for page in range(1, pages + 1):
        response = requests.get(
            f"{BASE_URL}/animals",
            headers=headers,
            params={"type": animal_type, "page": page, "limit": 100},
        )
        response.raise_for_status()
        batch = response.json().get("animals", [])
        if not batch:
            break
        animals.extend(batch)
        print(f"Fetched page {page} for {animal_type}: {len(batch)} records")

    return animals


def extract() -> list[dict]:
    dogs = fetch_animals("dog")
    cats = fetch_animals("cat")
    return dogs + cats
