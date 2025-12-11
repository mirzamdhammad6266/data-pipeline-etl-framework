"""
Simple ETL driver script.

This module wires together:
- ingestion.load_raw_dataframe
- ingestion.validate_raw_schema
- transform.enrich_features
- validation.run_quality_checks
- validation.filter_invalid_rows

It is designed to be easy to read in interviews and code reviews.
"""

from pathlib import Path

import pandas as pd

from . import ingestion, transform, validation


def run_etl(input_csv: str, output_csv: str) -> None:
    print(f"[ETL] Loading raw data from {input_csv!r}")
    raw_df = ingestion.load_raw_dataframe(input_csv)

    print(f"[ETL] Validating raw schema...")
    valid_df, invalid_count = ingestion.validate_raw_schema(raw_df)
    print(f"[ETL] Dropped {invalid_count} rows that failed schema validation.")

    print("[ETL] Enriching features...")
    enriched_df = transform.enrich_features(valid_df)

    print("[ETL] Running data-quality checks...")
    quality_report = validation.run_quality_checks(enriched_df)
    for check_name, value in quality_report.items():
        print(f"    {check_name}: {value}")

    print("[ETL] Filtering invalid rows based on quality checks...")
    cleaned_df = validation.filter_invalid_rows(enriched_df)

    output_path = Path(output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(output_path, index=False)

    print(f"[ETL] Pipeline complete. Wrote {len(cleaned_df)} rows to {output_csv!r}")


if __name__ == "__main__":
    # Example paths (can be changed when running locally)
    input_file = "data/raw_customers.csv"
    output_file = "data/clean_customers.csv"

    try:
        run_etl(input_file, output_file)
    except FileNotFoundError:
        # Helpful message if the example CSV has not been created yet
        print(
            "Input file not found. Put a CSV at 'data/raw_customers.csv' "
            "with columns: customer_id, signup_date, feature_1, feature_2, country"
        )
