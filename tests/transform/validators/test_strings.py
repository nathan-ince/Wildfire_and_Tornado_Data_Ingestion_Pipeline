import pandas as pd
import pytest

from project.transform.validators.strings import (
    validate_string_max_length,
    validate_string_exact_length,
)


def test_validate_string_max_length():
    df = pd.DataFrame(
        {
            "month": ["December", "TooLongMonthName", "", pd.NA],
        }
    )

    accepted, rejected = validate_string_max_length(df, "month", 9)

    assert len(accepted) == 1
    assert len(rejected) == 3
    assert rejected["rejected_reason"].iloc[0] == "invalid value :: field name = month"


def test_validate_string_exact_length():
    df = pd.DataFrame(
        {
            "state": ["NC", "B", "", pd.NA],
        }
    )

    accepted, rejected = validate_string_exact_length(df, "state", 2)

    assert len(accepted) == 1
    assert len(rejected) == 3
    assert rejected["rejected_reason"].iloc[0] == "invalid value :: field name = state"