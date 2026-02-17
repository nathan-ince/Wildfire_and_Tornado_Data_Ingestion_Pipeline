import pandas as pd
import pytest

from project.pipelines.wildfire_global import validators


@pytest.mark.parametrize(
    "fn, col, values, expected",
    [
        (validators.validate_country, "country", [" usa ", "canada", None], ["Usa", "Canada"]),
        (validators.validate_region, "region", [" north america ", "europe", None], ["North America", "Europe"]),
        (validators.validate_month, "month", [" january ", "december", "thisisacoolmonth"], ["January", "December"]),
    ],
)
def test_string_validators(fn, col, values, expected):
    df = pd.DataFrame({col: values})

    accepted, rejected = fn(df)

    assert accepted[col].tolist() == expected
    assert rejected.shape[0] == 1


def test_validate_handles_missing_values():
    df = pd.DataFrame({"cause": [" Nathan ", None, "Jack"]})

    accepted, rejected = validators.validate_cause(df)

    assert accepted["cause"].tolist() == ["lightning", "Unknown", "Human"]
    assert rejected.empty