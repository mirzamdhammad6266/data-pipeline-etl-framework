import pandas as pd


def enrich_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived features used by downstream ML models.

    - feature_sum = feature_1 + feature_2
    - is_high_value = feature_sum > threshold
    - signup_day = day of month extracted from signup_date
    """
    result = df.copy()

    # Ensure signup_date is a datetime column
    result["signup_date"] = pd.to_datetime(result["signup_date"])

    result["feature_sum"] = result["feature_1"] + result["feature_2"]
    result["is_high_value"] = result["feature_sum"] > 10.0
    result["signup_day"] = result["signup_date"].dt.day

    # Normalise missing country values
    result["country"] = result["country"].fillna("UNKNOWN")

    return result
