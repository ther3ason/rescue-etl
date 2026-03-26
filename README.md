# Rescue Animal ETL Pipeline

A Data Engineering portfolio project that extracts animal shelter intake and outcome records from municipal open data portals (via the Socrata API), joins them to compute shelter metrics, and loads the result into a local SQLite database.

**No API key required.** Data is sourced from publicly funded city open data portals.

## Project Structure

```
rescue-etl/
├── src/
│   ├── extract.py      # Paginated Socrata API fetcher (multi-city config)
│   ├── transform.py    # Schema normalization, join, and derived metrics
│   └── load.py         # Full-refresh load into SQLite
├── main.py             # Pipeline orchestrator
└── requirements.txt
```

## Data Sources

| City | Portal | Datasets |
|---|---|---|
| Austin, TX | data.austintexas.gov | Animal Center Intakes + Outcomes |

The pipeline is designed to support multiple cities — add a new source by appending an entry to the `SOURCES` list in `src/extract.py`.

## Setup

```bash
pip install -r requirements.txt
python main.py
```

Results are written to `rescue.db`.

## Schema

| Column | Type | Description |
|---|---|---|
| animal_id | TEXT | Shelter-assigned ID |
| source_city / source_state | TEXT | Which city's data portal |
| name | TEXT | Animal's name |
| animal_type | TEXT | `Dog` or `Cat` |
| breed | TEXT | Breed description |
| color | TEXT | Color description |
| gender | TEXT | `Male` or `Female` |
| neutered | INTEGER | 1 = fixed, 0 = intact |
| age_upon_intake | TEXT | e.g. `2 years`, `4 months` |
| intake_type | TEXT | `Stray`, `Owner Surrender`, etc. |
| intake_condition | TEXT | `Normal`, `Injured`, etc. |
| intake_datetime | TEXT | ISO 8601 |
| outcome_type | TEXT | `Adoption`, `Transfer`, `Return to Owner`, etc. |
| outcome_subtype | TEXT | Additional outcome detail |
| outcome_datetime | TEXT | ISO 8601 (`NULL` if still in shelter) |
| days_in_shelter | REAL | Outcome datetime − intake datetime in days |

## What This Demonstrates

- **Multi-endpoint extraction** with paginated Socrata API calls
- **Schema normalization** — parsing free-text fields (e.g. `"Neutered Male"` → `gender=Male, neutered=1`)
- **Dataset joining** — intakes left-joined to latest outcome per animal, enabling time-to-adoption analysis
- **Derived metrics** — `days_in_shelter` computed from joined timestamps
- **Full-refresh load pattern** with explicit DDL and SQLite upsert safety
- **Config-driven multi-source design** — adding a new city requires one dict entry
