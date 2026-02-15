import pandas as pd
import pytest

from project.transform.validators.presence import validate_notna


@pytest.mark.parametrize(
    "column, values, expected_valid, expected_invalid",
    [
        # Wildfire columns
        ("country", ["Turkey", None], ["Turkey"], [None]),
        ("year", [2000, None], [2000], [None]),
        ("month", [5, None], [5], [None]),
        ("region", ["Mugla", None], ["Mugla"], [None]),
        ("fires_count", [200, None], [200], [None]),
        ("burned_area_hectres", [4000, None], [4000], [None]),
        ("cause", ["Lightning", None], ["Lightning"], [None]),
        ("temperature_celsius", [30, None], [30], [None]),
        ("humidity_percent", [40, None], [40], [None]),
        ("wind_speed_kmh", [60, None], [60], [None]),

        # Tornado columns
        ("day", [7, None], [7], [None]),
        ("state", ["NC", None], ["NC"], [None]),
        ("magnitude", [4, None], [4], [None]),
        ("injury_count", [2, None], [2], [None]),
        ("fatality_count", [5, None], [5], [None]),
        ("latitude_start", [70, None], [70], [None]),
        ("latitude_end", [20, None], [20], [None]),
        ("longitude_start", [120, None], [120], [None]),
        ("longitude_end", [140, None], [140], [None]),
        ("length_miles", [8, None], [8], [None]),
        ("width_yards", [8, None], [8], [None]),
    ],
)
def test_validate_notna(column, values, expected_valid, expected_invalid):
    df = pd.DataFrame({column: values})
    accepted, rejected = validate_notna(df, column)

    assert accepted[column].tolist() == expected_valid
    assert rejected[column].tolist() == expected_invalid
    assert rejected["reason"].eq(f"invalid value :: field name = {column}").all()