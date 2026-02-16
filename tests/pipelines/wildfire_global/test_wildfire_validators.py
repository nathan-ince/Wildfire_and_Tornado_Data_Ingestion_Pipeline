import pandas as pd

from project.pipelines.wildfire_global import validators


def test_validate_country_strips_and_titles():
    df = pd.DataFrame({
        "country": [" usa ", "canada", None]
    })

    accepted, rejected = validators.validate_country(df)

    assert accepted["country"].tolist() == ["Usa", "Canada"]
    assert rejected.shape[0] == 1


def test_validate_month_max_length_and_title():
    df = pd.DataFrame({
        "month": [" january ", "february", "thismonthiswaytoolong"]
    })

    accepted, rejected = validators.validate_month(df)

    assert accepted["month"].tolist() == ["January", "February"]
    assert rejected.shape[0] == 1
    assert "month" in rejected["rejected_reason"].iloc[0]


def test_validate_region_strips_and_titles():
    df = pd.DataFrame({
        "region": [" north america ", "europe", None]
    })

    accepted, rejected = validators.validate_region(df)

    assert accepted["region"].tolist() == ["North America", "Europe"]
    assert rejected.shape[0] == 1


def test_validate_cause_fills_unknown_and_never_rejects():
    df = pd.DataFrame({
        "cause": [" lightning ", None, "Human"]
    })

    accepted, rejected = validators.validate_cause(df)

    assert accepted["cause"].tolist() == ["lightning", "Unknown", "Human"]
    assert rejected.empty