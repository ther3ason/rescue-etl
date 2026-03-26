import argparse
from src.extract import extract
from src.transform import transform
from src.load import load

VALID_LIMITS = [100, 1000, 10000]


def run_pipeline(limit: int):
    print(f"=== Extract (limit: {limit:,} records per dataset) ===")
    raw = extract(limit=limit)

    print("\n=== Transform ===")
    df = transform(raw)

    print("\n=== Load ===")
    load(df)

    print("\nPipeline complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the rescue animal ETL pipeline.")
    parser.add_argument(
        "--limit",
        type=int,
        choices=VALID_LIMITS,
        default=1000,
        help="Max records to fetch per dataset (default: 1000)",
    )
    args = parser.parse_args()
    run_pipeline(limit=args.limit)
