import logging
import pandas as pd

from project.models import Config
from project.utils import (
  rename_columns,
  run_main_process,
)
from project.utils.process import (
  process_between_int,
  process_duplicates_all_columns_keep_first,
  process_gte_zero,
  process_latitude,
  process_longitude,
  process_string_notna_exactly_n_characters,
  process_chain
)

logger = logging.getLogger(__name__)

def process_year(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df["year"].notna()
  recovery_mask = ~valid_mask & df["date"].notna()
  recovery_dates = df.loc[recovery_mask, "date"].astype("date32[pyarrow]") # works without astype, but type checker complains
  df.loc[recovery_mask, "year"] = recovery_dates.dt.year.astype("int16[pyarrow]")
  valid_mask = df["year"].notna()
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = "invalid value :: year"
  return df_accepted, df_rejected

def process_month(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df["month"].notna() & df["month"].between(1, 12)
  recovery_mask = ~valid_mask & df["date"].notna()
  recovery_dates = df.loc[recovery_mask, "date"].astype("date32[pyarrow]") # works without astype, but type checker complains
  df.loc[recovery_mask, "month"] = recovery_dates.dt.month.astype("int16[pyarrow]")
  valid_mask = df["month"].notna()
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = "invalid value :: month"
  return df_accepted, df_rejected

def process_day(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df["day"].notna() & df["day"].between(1, 31)
  recovery_mask = ~valid_mask & df["date"].notna()
  recovery_dates = df.loc[recovery_mask, "date"].astype("date32[pyarrow]") # works without astype, but type checker complains
  df.loc[recovery_mask, "day"] = recovery_dates.dt.day.astype("int16[pyarrow]")
  valid_mask = df["day"].notna() & df["day"].between(1, 31)
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = "invalid value :: day"
  return df_accepted, df_rejected

def process_date(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  recovery_mask = df["date"].isna() & df["year"].notna() & df["month"].notna() & df["day"].notna()
  df.loc[recovery_mask, "date"] = pd.to_datetime(df.loc[recovery_mask, ["year", "month", "day"]], errors="coerce").astype("date32[pyarrow]")
  valid_mask = df["date"].notna()
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = "invalid value :: date"
  return df_accepted, df_rejected

# validation for a combination of fields
# must occur after the individual validations above
def process_year_month_day_date(df: pd.DataFrame):
  valid_mask = df["year"].notna() & df["month"].notna() & df["day"].notna() & df["date"].notna()
  df_accepted = df.loc[valid_mask]
  df_rejected = df.loc[~valid_mask]
  df_rejected["reason"] = "invalid combination of values :: year, month, or day is N/A :: date is N/A"
  return df_accepted, df_rejected

def process_state(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  df_accepted, df_rejected = process_string_notna_exactly_n_characters(df, "state", 2)
  df_accepted["state"] = df["state"].str.strip().str.upper()
  return df_accepted, df_rejected

def process_magnitude(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  return process_between_int(df, "magnitude", 0, 5)

def process_injury_count(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  return process_gte_zero(df, "injury_count")

def process_fatality_count(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  return process_gte_zero(df, "fatality_count")

def process_latitude_start(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  return process_latitude(df, "latitude_start")

def process_longitude_start(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  return process_longitude(df, "longitude_start")

def process_latitude_end(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  return process_latitude(df, "latitude_end")

def process_longitude_end(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  return process_longitude(df, "longitude_end")

def process_length_miles(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  return process_gte_zero(df, "length_miles")

def process_width_yards(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  return process_gte_zero(df, "width_yards")

def transform_data_completely(config: Config, source_index: int, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  logger.info("transforming data")
  df = rename_columns(config, source_index, df)
  result = process_chain(df, (
    process_year,
    process_month,
    process_day,
    process_date,
    process_state,
    process_magnitude,
    process_injury_count,
    process_fatality_count,
    process_latitude_start,
    process_longitude_start,
    process_latitude_end,
    process_longitude_end,
    process_length_miles,
    process_width_yards,
    process_year_month_day_date, # intentionally here
    process_duplicates_all_columns_keep_first # intentionally last
  ))
  logger.info("transformed data")
  return result

def start(): run_main_process("config/tornado_usa.yaml", transform_data_completely)

__all__ = ["start"]
