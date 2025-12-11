from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date


class RawRecord(BaseModel):
    """Shape of the raw data coming from the CSV/source system."""
    customer_id: int
    signup_date: date
    feature_1: float
    feature_2: float
    country: Optional[str] = Field(default=None)


class CleanRecord(BaseModel):
    """Validated & transformed record used by downstream ML workflows."""
    customer_id: int
    signup_day: int
    feature_1: float
    feature_2: float
    feature_sum: float
    is_high_value: bool
    country: str = "UNKNOWN"

    @validator("feature_sum")
    def sum_must_be_consistent(cls, v, values):
        f1 = values.get("feature_1")
        f2 = values.get("feature_2")
        if f1 is not None and f2 is not None:
            expected = f1 + f2
            # allow small float rounding difference
            if abs(expected - v) > 1e-6:
                raise ValueError("feature_sum must equal feature_1 + feature_2")
        return v
