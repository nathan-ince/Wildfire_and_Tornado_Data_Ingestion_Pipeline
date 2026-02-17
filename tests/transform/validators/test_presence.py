import pandas as pd
import pytest

from project.transform.validators.presence import validate_notna


@pytest.mark.parametrize(
    "column",
    [
        # Wildfire
        "country",
        "year",
        "month",
        "region",
        "fires_count",
        "burned_area_hectres",
        "cause",
        "temperature_celsius",
        "humidity_percent",
        "wind_speed_kmh",

        # Tornado
        "day",
        "state",
        "magnitude",
        "injury_count",
        "fatality_count",
        "latitude_start",
        "latitude_end",
        "longitude_start",
        "longitude_end",
        "length_miles",
        "width_yards",
    ],
)
def test_validate_notna(column):
    df = pd.DataFrame({column: [1, pd.NA]})

    accepted, rejected = validate_notna(df, column)

    assert len(accepted) == 1
    assert len(rejected) == 1
    assert rejected["rejected_reason"].iloc[0] == f"invalid value :: field name = {column}"