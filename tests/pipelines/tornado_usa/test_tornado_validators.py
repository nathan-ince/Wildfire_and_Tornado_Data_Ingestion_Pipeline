import pandas as pd
import pytest

from project.pipelines.tornado_usa import validators


@pytest.mark.parametrize(
    "col, expected",
    [
        ("year", 2019),
        ("month", 5),
        ("day", 10),
    ],
)
def test_validate_recovers_from_date(col, expected):
    df = pd.DataFrame(
        {
            col: [None],
            "date": [pd.Timestamp("2019-05-10")],
        }
    )

    accepted, rejected = getattr(validators, f"validate_{col}")(df)

    assert rejected.empty
    assert accepted[col].iloc[0] == expected


def test_validate_date_recovers_from_year_month_day():
    df = pd.DataFrame(
        {
            "year": [2019, None],
            "month": [5, 1],
            "day": [10, 1],
            "date": [None, None],
        }
    )

    accepted, rejected = validators.validate_date(df)

    assert accepted.shape[0] == 1
    assert rejected.shape[0] == 1
    assert str(accepted["date"].iloc[0])[:10] == "2019-05-10"
    assert rejected["rejected_reason"].iloc[0] == "invalid value :: date"


def test_validate_state_normalizes():
    df = pd.DataFrame({"state": [" nc ", "CA", None]})

    accepted, rejected = validators.validate_state(df)

    assert accepted["state"].tolist() == ["NC", "CA"]
    assert rejected.shape[0] == 1


def test_validate_year_month_day_date_combination():
    df = pd.DataFrame(
        {
            "year": [2020, None],
            "month": [1, 1],
            "day": [1, 1],
            "date": [pd.Timestamp("2020-01-01"), pd.Timestamp("2020-01-01")],
        }
    )

    accepted, rejected = validators.validate_year_month_day_date(df)

    assert accepted.shape[0] == 1
    assert rejected.shape[0] == 1
    assert rejected["rejected_reason"].iloc[0] == "invalid combination :: year/month/day/date"