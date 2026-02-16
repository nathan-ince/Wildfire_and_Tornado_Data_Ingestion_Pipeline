import pandas as pd
import pytest

from project.transform.validators.presence import validate_notna

def to_py_list(values) -> list:
    s = pd.Series(values)
    return s.astype(object).where(s.notna(), None).tolist()


@pytest.mark.parametrize(
    "column, values, expected_valid, expected_invalid",
    [
        # Wildfire
        ("country", ["Turkey", pd.NA], ["Turkey"], [pd.NA]),
        ("year", [2000, pd.NA], [2000], [pd.NA]),
        ("month", [5, pd.NA], [5], [pd.NA]),
        ("region", ["Mugla", pd.NA], ["Mugla"], [pd.NA]),
        ("fires_count", [200, pd.NA], [200], [pd.NA]),
        ("burned_area_hectres", [4000, pd.NA], [4000], [pd.NA]),
        ("cause", ["Lightning", pd.NA], ["Lightning"], [pd.NA]),
        ("temperature_celsius", [30, pd.NA], [30], [pd.NA]),
        ("humidity_percent", [40, pd.NA], [40], [pd.NA]),
        ("wind_speed_kmh", [60, pd.NA], [60], [pd.NA]),

        # Tornado
        ("day", [7, pd.NA], [7], [pd.NA]),
        ("state", ["NC", pd.NA], ["NC"], [pd.NA]),
        ("magnitude", [4, pd.NA], [4], [pd.NA]),
        ("injury_count", [2, pd.NA], [2], [pd.NA]),
        ("fatality_count", [5, pd.NA], [5], [pd.NA]),
        ("latitude_start", [70, pd.NA], [70], [pd.NA]),
        ("latitude_end", [20, pd.NA], [20], [pd.NA]),
        ("longitude_start", [120, pd.NA], [120], [pd.NA]),
        ("longitude_end", [140, pd.NA], [140], [pd.NA]),
        ("length_miles", [8, pd.NA], [8], [pd.NA]),
        ("width_yards", [8, pd.NA], [8], [pd.NA]),
    ],
)
def test_validate_notna(column, values, expected_valid, expected_invalid):
    df = pd.DataFrame({column: values})
    accepted, rejected = validate_notna(df, column)

    assert to_py_list(accepted[column]) == to_py_list(expected_valid)
    assert to_py_list(rejected[column]) == to_py_list(expected_invalid)
    assert rejected["reason"].eq(f"invalid value :: field name = {column}").all()