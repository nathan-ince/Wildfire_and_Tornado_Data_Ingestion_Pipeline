import pandas as pd
import pytest

from project.transform.validators.numeric import validate_int_between, validate_non_negative


@pytest.mark.parametrize(
    "column, values, expected_valid, expected_invalid",
    [
        # Wildfire
        ("year", [-700, 2000, None], [2000], [-700, None]),
        ("fires_count", [-40, 300, None], [300], [-40, None]),
        ("burned_area_hectres", [-8000, 70000, None], [70000], [-8000, None]),
        ("temperature_celsius", [-60, 20, None], [20], [-60, None]),
        ("wind_speed_kmh", [-70, 10, None], [10], [-70, None]),

        # Tornado
        ("injury_count", [-7, 2, None], [2], [-7, None]),
        ("fatality_count", [-4, 1, None], [1], [-4, None]),
        ("length_miles", [-10, 30, None], [30], [-10, None]),
        ("width_yards", [-20, 60, None], [60], [-20, None]),
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
        ("humidity_percent", [0, -10, 5, None], 0, 100, [0, 5], [-10, None]),

        # Tornado
        ("month", [0, -10, 5, None], 1, 12, [5], [0, -10, None]),
        ("day", [0, -10, 20, None], 1, 31, [20], [0, -10, None]),
        ("magnitude", [-1, 3, None], 0, 5, [3], [-1, None]),
    ],
)
def test_validate_int_between(column, values, left, right, expected_valid, expected_invalid):
    df = pd.DataFrame({column: values})
    accepted, rejected = validate_int_between(df, column, left, right)

    assert accepted[column].tolist() == expected_valid
    assert rejected[column].tolist() == expected_invalid
    assert rejected["reason"].eq(f"invalid value :: field name = {column}").all()