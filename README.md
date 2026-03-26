# Rescue Animal ETL Pipeline

A Data Engineering portfolio project that extracts dog and cat rescue listings from the [Petfinder API](https://www.petfinder.com/developers/), transforms the raw data into a clean tabular format, and loads it into a local SQLite database.

## Project Structure

```
rescue-etl/
├── src/
│   ├── extract.py      # Pulls raw animal records from the Petfinder API
│   ├── transform.py    # Flattens and cleans records into a pandas DataFrame
│   └── load.py         # Upserts the DataFrame into a SQLite database
├── main.py             # Orchestrates the full ETL pipeline
├── requirements.txt
└── .env.example
```

## Setup

1. **Clone the repo and install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** from the example template:

   ```bash
   cp .env.example .env
   ```

3. **Register for a free Petfinder API key** at https://www.petfinder.com/developers/ and add your credentials to `.env`:

   ```
   PETFINDER_API_KEY=your_api_key_here
   PETFINDER_SECRET=your_secret_here
   ```

## Usage

Run the full pipeline:

```bash
python main.py
```

This will:
1. Authenticate with the Petfinder API and fetch dog and cat listings (up to 3 pages each by default)
2. Flatten nested JSON fields, parse timestamps, and deduplicate records
3. Write the results to `rescue.db` (SQLite) in an `animals` table

## Schema

| Column | Type | Description |
|---|---|---|
| id | INTEGER (PK) | Petfinder animal ID |
| name | TEXT | Animal's name |
| type | TEXT | `Dog` or `Cat` |
| breed_primary | TEXT | Primary breed |
| age | TEXT | `Baby`, `Young`, `Adult`, `Senior` |
| gender | TEXT | `Male` or `Female` |
| size | TEXT | `Small`, `Medium`, `Large`, `Extra Large` |
| status | TEXT | `adoptable`, `adopted`, etc. |
| spayed_neutered | INTEGER | Boolean |
| house_trained | INTEGER | Boolean |
| org_id | TEXT | Rescue organization ID |
| city / state | TEXT | Location |
| published_at | TEXT | ISO 8601 timestamp |
| url | TEXT | Petfinder listing URL |

## Why This Project

This pipeline demonstrates core data engineering skills:
- **REST API authentication** (OAuth2 client credentials flow)
- **Incremental extraction** with pagination
- **Data normalization** of nested JSON using pandas
- **Relational storage** with SQLite
- **Environment-based configuration** for secrets management
