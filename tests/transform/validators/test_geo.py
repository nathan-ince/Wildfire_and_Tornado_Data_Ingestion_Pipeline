import pandas as pd
import pytest

from project.transform.validators.geo import validate_latitude, validate_longitude


@pytest.mark.parametrize(
    "column, values, expected_valid, expected_invalid",
    [
        # Tornado
        ("latitude_start", [-100, -80, 0, 80, 100, pd.NA], [-80, 0, 80], [-100, 100, pd.NA]),
        ("latitude_end",   [-100, -80, 0, 80, 100, pd.NA], [-80, 0, 80], [-100, 100, pd.NA]),
    ],
)
def test_validate_latitude(column, values, expected_valid, expected_invalid):
    df = pd.DataFrame({column: values})
    accepted, rejected = validate_latitude(df, column)

    assert accepted[column].tolist() == expected_valid
    assert rejected[column].tolist() == expected_invalid
    assert rejected["rejected_reason"].eq(f"invalid value :: field name = {column}").all()


@pytest.mark.parametrize(
    "column, values, expected_valid, expected_invalid",
    [
        # Tornado
        ("longitude_start", [-200, -180, 0, 180, 200, pd.NA], [-180, 0, 180], [-200, 200, pd.NA]),
        ("longitude_end",   [-200, -180, 0, 180, 200, pd.NA], [-180, 0, 180], [-200, 200, pd.NA]),
    ],
)
def test_validate_longitude(column, values, expected_valid, expected_invalid):
    df = pd.DataFrame({column: values})
    accepted, rejected = validate_longitude(df, column)

    assert accepted[column].tolist() == expected_valid
    assert rejected[column].tolist() == expected_invalid
    assert rejected["rejected_reason"].eq(f"invalid value :: field name = {column}").all()