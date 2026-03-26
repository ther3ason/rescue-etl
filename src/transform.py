import pandas as pd

ANIMAL_TYPES = {"Dog", "Cat"}


def _parse_sex(sex_str: str | None) -> tuple[str | None, bool | None]:
    """Parse Socrata sex field into gender and fixed status.

    Examples:
        'Neutered Male'  -> ('Male', True)
        'Spayed Female'  -> ('Female', True)
        'Intact Male'    -> ('Male', False)
        'Unknown'        -> (None, None)
    """
    if not sex_str or sex_str.strip().lower() == "unknown":
        return None, None
    parts = sex_str.strip().split()
    if len(parts) == 2:
        fixed_word, gender = parts[0].lower(), parts[1]
        neutered = fixed_word in ("neutered", "spayed")
        return gender, neutered
    return sex_str, None


def _normalize_intakes(records: list[dict]) -> pd.DataFrame:
    rows = []
    for r in records:
        gender, neutered = _parse_sex(r.get("sex_upon_intake"))
        rows.append(
            {
                "animal_id": r.get("animal_id"),
                "source_city": r.get("_source_city"),
                "source_state": r.get("_source_state"),
                "name": r.get("name"),
                "animal_type": r.get("animal_type"),
                "breed": r.get("breed"),
                "color": r.get("color"),
                "gender": gender,
                "neutered": neutered,
                "age_upon_intake": r.get("age_upon_intake"),
                "intake_type": r.get("intake_type"),
                "intake_condition": r.get("intake_condition"),
                "intake_datetime": r.get("datetime"),
            }
        )
    df = pd.DataFrame(rows)
    df["intake_datetime"] = pd.to_datetime(df["intake_datetime"], errors="coerce", utc=True)
    return df


def _normalize_outcomes(records: list[dict]) -> pd.DataFrame:
    rows = []
    for r in records:
        rows.append(
            {
                "animal_id": r.get("animal_id"),
                "source_city": r.get("_source_city"),
                "outcome_type": r.get("outcome_type"),
                "outcome_subtype": r.get("outcome_subtype"),
                "outcome_datetime": r.get("datetime"),
            }
        )
    df = pd.DataFrame(rows)
    df["outcome_datetime"] = pd.to_datetime(df["outcome_datetime"], errors="coerce", utc=True)
    return df


def transform(raw: dict[str, list[dict]]) -> pd.DataFrame:
    """Normalize, join, and enrich intake and outcome records."""
    intakes = _normalize_intakes(raw["intakes"])
    outcomes = _normalize_outcomes(raw["outcomes"])

    # Filter to dogs and cats only
    intakes = intakes[intakes["animal_type"].isin(ANIMAL_TYPES)].copy()

    # Keep only the most recent outcome per animal per city
    latest_outcomes = (
        outcomes.sort_values("outcome_datetime")
        .groupby(["animal_id", "source_city"], as_index=False)
        .last()
    )

    # Left join: intakes without outcomes remain in the dataset (still in shelter)
    df = intakes.merge(
        latest_outcomes[["animal_id", "source_city", "outcome_type", "outcome_subtype", "outcome_datetime"]],
        on=["animal_id", "source_city"],
        how="left",
    )

    # Derived metric: days from intake to outcome
    df["days_in_shelter"] = (df["outcome_datetime"] - df["intake_datetime"]).dt.days

    df.drop_duplicates(subset=["animal_id", "source_city", "intake_datetime"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    print(f"Transformed {len(df):,} records")
    print(f"  By type:    {df['animal_type'].value_counts().to_dict()}")
    print(f"  By outcome: {df['outcome_type'].value_counts().head(5).to_dict()}")
    return df
