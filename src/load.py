import sqlite3
import pandas as pd

DB_PATH = "rescue.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS animals (
    animal_id        TEXT,
    source_city      TEXT,
    source_state     TEXT,
    name             TEXT,
    animal_type      TEXT,
    breed            TEXT,
    color            TEXT,
    gender           TEXT,
    neutered         INTEGER,
    age_upon_intake  TEXT,
    intake_type      TEXT,
    intake_condition TEXT,
    intake_datetime  TEXT,
    outcome_type     TEXT,
    outcome_subtype  TEXT,
    outcome_datetime TEXT,
    days_in_shelter  REAL,
    PRIMARY KEY (animal_id, source_city, intake_datetime)
)
"""


def load(df: pd.DataFrame, db_path: str = DB_PATH) -> None:
    """Full-refresh load: drop, recreate, and insert all records."""
    df = df.copy()

    # SQLite has no native boolean — convert to 0/1
    df["neutered"] = df["neutered"].map({True: 1, False: 0})

    # Convert timestamps to ISO strings
    for col in ("intake_datetime", "outcome_datetime"):
        df[col] = df[col].dt.strftime("%Y-%m-%dT%H:%M:%S%z").where(df[col].notna(), None)

    with sqlite3.connect(db_path) as conn:
        conn.execute("DROP TABLE IF EXISTS animals")
        conn.execute(CREATE_TABLE_SQL)
        df.to_sql("animals", conn, if_exists="append", index=False, method="multi")

        row_count = conn.execute("SELECT COUNT(*) FROM animals").fetchone()[0]
        print(f"Load complete. {row_count:,} rows in animals table ({db_path})")
