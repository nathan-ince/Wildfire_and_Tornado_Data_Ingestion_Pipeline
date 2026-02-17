import pandas as pd

NUMERIC_COLS = [
    "year", "month", "day",
    "magnitude", "injury_count", "fatality_count",
    "latitude_start", "latitude_end",
    "longitude_start", "longitude_end",
    "length_miles", "width_yards"
]

def clean_tornado_usa(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # text conversion
    if "state" in df.columns:
        df["state"] = df["state"].astype("string").str.strip().str.upper()

    # numeric conversion
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")


    # date conversion
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    else:
        df["date"] = pd.to_datetime(
            df[["year", "month", "day"]],
            errors="coerce"
        ).dt.date

    return df

__all__ = ["clean_tornado_usa"]