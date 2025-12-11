from typing import Dict

import pandas as pd


def run_quality_checks(df: pd.DataFrame) -> Dict[str, int]:
    """
    Run simple data-quality checks.

    Returns a dictionary with counts that can be logged or monitored:
      - missing_feature_1
      - missing_feature_2
      - negative_feature_1
      - negative_feature_2
    """
    checks = {
        "missing_feature_1": int(df["feature_1"].isna().sum()),
        "missing_feature_2": int(df["feature_2"].isna().sum()),
        "negative_feature_1": int((df["feature_1"] < 0).sum()),
        "negative_feature_2": int((df["feature_2"] < 0).sum()),
    }
    return checks


def filter_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop rows that fail critical quality checks.

    - Remove rows with null feature_1 or feature_2
    - Remove rows where any feature is negative
    """
    mask = (
        df["feature_1"].notna()
        & df["feature_2"].notna()
        & (df["feature_1"] >= 0)
        & (df["feature_2"] >= 0)
    )
    return df[mask].reset_index(drop=True)
