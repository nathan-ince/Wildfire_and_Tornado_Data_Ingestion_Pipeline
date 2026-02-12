import pandas as pd

NUMERIC_COLS = [
    "year",
    "recorded_fires_count",
    "burned_area_hectares",
    "temperature_celsius",
    "humidity_percent",
    "wind_speed_kmh",
]

def clean_wildfire(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # text conversion
    for col in ["country", "month", "region", "cause"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    # numeric conversion
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

__all__ = ["clean_wildfire"]