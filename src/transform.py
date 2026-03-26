import pandas as pd


def transform(raw_animals: list[dict]) -> pd.DataFrame:
    """Flatten and clean raw API records into a normalized DataFrame."""
    records = []

    for animal in raw_animals:
        records.append(
            {
                "id": animal.get("id"),
                "name": animal.get("name"),
                "type": animal.get("type"),
                "breed_primary": animal.get("breeds", {}).get("primary"),
                "breed_secondary": animal.get("breeds", {}).get("secondary"),
                "age": animal.get("age"),
                "gender": animal.get("gender"),
                "size": animal.get("size"),
                "color_primary": animal.get("colors", {}).get("primary"),
                "status": animal.get("status"),
                "spayed_neutered": animal.get("attributes", {}).get("spayed_neutered"),
                "house_trained": animal.get("attributes", {}).get("house_trained"),
                "special_needs": animal.get("attributes", {}).get("special_needs"),
                "shots_current": animal.get("attributes", {}).get("shots_current"),
                "org_id": animal.get("organization_id"),
                "city": animal.get("contact", {}).get("address", {}).get("city"),
                "state": animal.get("contact", {}).get("address", {}).get("state"),
                "postcode": animal.get("contact", {}).get("address", {}).get("postcode"),
                "published_at": animal.get("published_at"),
                "url": animal.get("url"),
            }
        )

    df = pd.DataFrame(records)
    df["published_at"] = pd.to_datetime(df["published_at"], utc=True, errors="coerce")
    df.drop_duplicates(subset="id", inplace=True)
    df.reset_index(drop=True, inplace=True)

    print(f"Transformed {len(df)} records ({df['type'].value_counts().to_dict()})")
    return df
