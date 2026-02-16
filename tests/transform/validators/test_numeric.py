import pandas as pd
import pytest

from project.transform.validators.numeric import validate_int_between, validate_non_negative


@pytest.mark.parametrize(
    "column, values, expected_valid, expected_invalid",
    [
        # Wildfire
        ("year", [-700, 2000, pd.NA], [2000], [-700, pd.NA]),
        ("fires_count", [-40, 300, pd.NA], [300], [-40, pd.NA]),
        ("burned_area_hectres", [-8000, 70000, pd.NA], [70000], [-8000, pd.NA]),
        ("temperature_celsius", [-60, 20, pd.NA], [20], [-60, pd.NA]),
        ("wind_speed_kmh", [-70, 10, pd.NA], [10], [-70, pd.NA]),

        # Tornado
        ("injury_count", [-7, 2, pd.NA], [2], [-7, pd.NA]),
        ("fatality_count", [-4, 1, pd.NA], [1], [-4, pd.NA]),
        ("length_miles", [-10, 30, pd.NA], [30], [-10, pd.NA]),
        ("width_yards", [-20, 60, pd.NA], [60], [-20, pd.NA]),
    ],
)
def test_validate_non_negative(column, values, expected_valid, expected_invalid):
    df = pd.DataFrame({column: values})
    accepted, rejected = validate_non_negative(df, column)

    assert accepted[column].tolist() == expected_valid
    assert rejected[column].tolist() == expected_invalid
    assert rejected["reason"].eq(f"invalid value :: field name = {column}").all()


@pytest.mark.parametrize(
    "column, values, left, right, expected_valid, expected_invalid",
    [
        # Wildfire
        ("humidity_percent", [0, -10, 5, pd.NA], 0, 100, [0, 5], [-10, pd.NA]),

        # Tornado
        ("month", [0, -10, 5, pd.NA], 1, 12, [5], [0, -10, pd.NA]),
        ("day", [0, -10, 20, pd.NA], 1, 31, [20], [0, -10, pd.NA]),
        ("magnitude", [-1, 3, pd.NA], 0, 5, [3], [-1, pd.NA]),
    ],
)
def test_validate_int_between(column, values, left, right, expected_valid, expected_invalid):
    df = pd.DataFrame({column: values})
    accepted, rejected = validate_int_between(df, column, left, right)

    assert accepted[column].tolist() == expected_valid
    assert rejected[column].tolist() == expected_invalid
    assert rejected["reason"].eq(f"invalid value :: field name = {column}").all()