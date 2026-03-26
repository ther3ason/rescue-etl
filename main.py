from src.extract import extract
from src.transform import transform
from src.load import load


def run_pipeline():
    print("=== Extract ===")
    raw = extract()

    print("\n=== Transform ===")
    df = transform(raw)

    print("\n=== Load ===")
    load(df)

    print("\nPipeline complete.")


if __name__ == "__main__":
    run_pipeline()
