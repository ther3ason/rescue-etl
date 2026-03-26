import sqlite3
import pandas as pd

DB_PATH = "rescue.db"


def load(df: pd.DataFrame, db_path: str = DB_PATH) -> None:
    """Upsert transformed records into the SQLite animals table."""
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS animals (
                id INTEGER PRIMARY KEY,
                name TEXT,
                type TEXT,
                breed_primary TEXT,
                breed_secondary TEXT,
                age TEXT,
                gender TEXT,
                size TEXT,
                color_primary TEXT,
                status TEXT,
                spayed_neutered INTEGER,
                house_trained INTEGER,
                special_needs INTEGER,
                shots_current INTEGER,
                org_id TEXT,
                city TEXT,
                state TEXT,
                postcode TEXT,
                published_at TEXT,
                url TEXT
            )
        """)

        # Upsert: replace existing rows by primary key
        df.to_sql("animals", conn, if_exists="append", index=False, method="multi")

        row_count = conn.execute("SELECT COUNT(*) FROM animals").fetchone()[0]
        print(f"Load complete. Total rows in animals table: {row_count}")
