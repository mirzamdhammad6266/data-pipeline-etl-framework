from pathlib import Path
from typing import Tuple

import pandas as pd

from .models import RawRecord


def load_raw_dataframe(csv_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.

    The CSV is expected to contain columns:
    customer_id, signup_date, feature_1, feature_2, country (optional).
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {csv_path}")

    df = pd.read_csv(path)
    return df


def validate_raw_schema(df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
    """
    Validate raw rows against the RawRecord schema using Pydantic.

    Returns:
        (valid_rows_df, invalid_count)
    """
    valid_rows = []
    invalid_count = 0

    for _, row in df.iterrows():
        try:
            record = RawRecord(
                customer_id=row["customer_id"],
                signup_date=row["signup_date"],
                feature_1=row["feature_1"],
                feature_2=row["feature_2"],
                country=row.get("country"),
            )
            valid_rows.append(record.dict())
        except Exception:
            invalid_count += 1

    valid_df = pd.DataFrame(valid_rows)
    return valid_df, invalid_count
