import pandas as pd

from project.transform.validators.presence import validate_notna
from project.transform.validators.numeric import validate_int_between, validate_non_negative
from project.transform.validators.strings import validate_string_max_length, validate_string_exact_length
from project.transform.validators.geo import validate_latitude, validate_longitude


def validate_year(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_mask = df["year"].notna()

    recovery_mask = ~valid_mask & df["date"].notna()
    if recovery_mask.any():
        recovery_dates = df.loc[recovery_mask, "date"].astype("date32[pyarrow]")
        df.loc[recovery_mask, "year"] = recovery_dates.dt.year.astype("int16[pyarrow]")

    valid_mask = df["year"].notna()
    df_accepted = df[valid_mask]
    df_rejected = df[~valid_mask].copy()
    df_rejected["reason"] = "invalid value :: year"
    return df_accepted, df_rejected

def validate_month(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_mask = df["month"].notna() & df["month"].between(1, 12)

    recovery_mask = ~valid_mask & df["date"].notna()
    if recovery_mask.any():
        recovery_dates = df.loc[recovery_mask, "date"].astype("date32[pyarrow]")
        df.loc[recovery_mask, "month"] = recovery_dates.dt.month.astype("int16[pyarrow]")

    valid_mask = df["month"].notna() & df["month"].between(1, 12)
    df_accepted = df[valid_mask]
    df_rejected = df[~valid_mask].copy()
    df_rejected["reason"] = "invalid value :: month"
    return df_accepted, df_rejected

def validate_day(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_mask = df["day"].notna() & df["day"].between(1, 31)

    recovery_mask = ~valid_mask & df["date"].notna()
    if recovery_mask.any():
        recovery_dates = df.loc[recovery_mask, "date"].astype("date32[pyarrow]")
        df.loc[recovery_mask, "day"] = recovery_dates.dt.day.astype("int16[pyarrow]")

    valid_mask = df["day"].notna() & df["day"].between(1, 31)
    df_accepted = df[valid_mask]
    df_rejected = df[~valid_mask].copy()
    df_rejected["reason"] = "invalid value :: day"
    return df_accepted, df_rejected

def validate_date(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    recovery_mask = (
        df["date"].isna()
        & df["year"].notna()
        & df["month"].notna()
        & df["day"].notna()
    )
    if recovery_mask.any():
        df.loc[recovery_mask, "date"] = (
            pd.to_datetime(
                df.loc[recovery_mask, ["year", "month", "day"]],
                errors="coerce",
            )
            .astype("date32[pyarrow]")
        )

    valid_mask = df["date"].notna()
    df_accepted = df[valid_mask]
    df_rejected = df[~valid_mask].copy()
    df_rejected["reason"] = "invalid value :: date"
    return df_accepted, df_rejected

def validate_year_month_day_date(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_mask = (
        df["year"].notna()
        & df["month"].notna()
        & df["day"].notna()
        & df["date"].notna()
    )
    df_accepted = df.loc[valid_mask]
    df_rejected = df.loc[~valid_mask].copy()
    df_rejected["reason"] = "invalid combination :: year/month/day/date"
    return df_accepted, df_rejected

def validate_state(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df_accepted, df_rejected = validate_string_exact_length(df, "state", 2)
    df_accepted["state"] = df_accepted["state"].str.strip().str.upper()
    return df_accepted, df_rejected

def validate_magnitude(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return validate_int_between(df, "magnitude", 0, 5)

def validate_injury_count(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return validate_non_negative(df, "injury_count")

def validate_fatality_count(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return validate_non_negative(df, "fatality_count")

def validate_latitude_start(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return validate_latitude(df, "latitude_start")

def validate_longitude_start(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return validate_longitude(df, "longitude_start")

def validate_latitude_end(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return validate_latitude(df, "latitude_end")

def validate_longitude_end(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return validate_longitude(df, "longitude_end")

def validate_length_miles(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return validate_non_negative(df, "length_miles")

def validate_width_yards(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return validate_non_negative(df, "width_yards")