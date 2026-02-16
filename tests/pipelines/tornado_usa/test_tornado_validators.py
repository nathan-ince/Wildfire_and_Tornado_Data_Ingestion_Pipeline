import pandas as pd

from project.pipelines.tornado_usa import validators


def test_validate_year_recovers_from_date():
    df = pd.DataFrame({
        "year": [None, 2020],
        "date": [pd.Timestamp("2019-05-10"), pd.Timestamp("2020-01-01")],
    })

    accepted, rejected = validators.validate_year(df)

    assert rejected.empty
    assert accepted["year"].tolist() == [2019, 2020]


def test_validate_month_recovers_from_date():
    df = pd.DataFrame({
        "month": [None, 12],
        "date": [pd.Timestamp("2019-05-10"), pd.Timestamp("2020-12-01")],
    })

    accepted, rejected = validators.validate_month(df)

    assert rejected.empty
    assert accepted["month"].tolist() == [5, 12]


def test_validate_day_recovers_from_date():
    df = pd.DataFrame({
        "day": [None, 31],
        "date": [pd.Timestamp("2019-05-10"), pd.Timestamp("2020-12-31")],
    })

    accepted, rejected = validators.validate_day(df)

    assert rejected.empty
    assert accepted["day"].tolist() == [10, 31]


def test_validate_date_recovers_from_year_month_day():
    df = pd.DataFrame({
        "year": [2019, None],
        "month": [5, 1],
        "day": [10, 1],
        "date": [None, None],
    })

    accepted, rejected = validators.validate_date(df)

    assert accepted.shape[0] == 1
    assert rejected.shape[0] == 1
    assert str(accepted.iloc[0]["date"])[:10] == "2019-05-10"
    assert rejected["rejected_reason"].iloc[0] == "invalid value :: date"


def test_validate_state_strips_and_uppercasses():
    df = pd.DataFrame({"state": [" nc ", "CA", None]})

    accepted, rejected = validators.validate_state(df)

    assert accepted["state"].tolist() == ["NC", "CA"]
    assert rejected.shape[0] == 1
    assert "state" in rejected["rejected_reason"].iloc[0]


def test_validate_year_month_day_date_combination():
    df = pd.DataFrame({
        "year": [2020, None],
        "month": [1, 1],
        "day": [1, 1],
        "date": [pd.Timestamp("2020-01-01"), pd.Timestamp("2020-01-01")],
    })

    accepted, rejected = validators.validate_year_month_day_date(df)

    assert accepted.shape[0] == 1
    assert rejected.shape[0] == 1
    assert rejected["rejected_reason"].iloc[0] == "invalid combination :: year/month/day/date"