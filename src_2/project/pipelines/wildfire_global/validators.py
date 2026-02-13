import pandas as pd

from project.transform.validators.presence import validate_notna
from project.transform.validators.numeric import validate_int_between, validate_non_negative
from project.transform.validators.strings import validate_string_max_length

def validate_country(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df_accepted, df_rejected = validate_notna(df, "country")
    df_accepted["country"] = df_accepted["country"].str.strip().str.title()
    return df_accepted, df_rejected

def validate_year(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return validate_notna(df, "year")

def validate_month(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df_accepted, df_rejected = validate_string_max_length(df, "month", 9)
    df_accepted["month"] = df_accepted["month"].str.strip().str.title()
    return df_accepted, df_rejected

def validate_region(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df_accepted, df_rejected = validate_notna(df, "region")
    df_accepted["region"] = df_accepted["region"].str.strip().str.title()
    return df_accepted, df_rejected

def validate_fires_count(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return validate_non_negative(df, "fires_count")

def validate_burned_area_hectares(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return validate_non_negative(df, "burned_area_hectares")

def validate_cause(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    # normalize missing -> "Unknown"; never reject
    missing_mask = df["cause"].isna()
    if missing_mask.any():
        df.loc[missing_mask, "cause"] = "Unknown"
    df["cause"] = df["cause"].str.strip()

    df_rejected = df.iloc[0:0].copy()
    df_rejected["reason"] = pd.Series(dtype="string[pyarrow]")
    return df, df_rejected

def validate_temperature_celsius(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return validate_notna(df, "temperature_celsius")

def validate_humidity_percent(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return validate_int_between(df, "humidity_percent", 0, 100)

def validate_wind_speed_kmh(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return validate_non_negative(df, "wind_speed_kmh")


__all__ = [
    "validate_country",
    "validate_year",
    "validate_month",
    "validate_region",
    "validate_fires_count",
    "validate_burned_area_hectares",
    "validate_cause",
    "validate_temperature_celsius",
    "validate_humidity_percent",
    "validate_wind_speed_kmh",
]