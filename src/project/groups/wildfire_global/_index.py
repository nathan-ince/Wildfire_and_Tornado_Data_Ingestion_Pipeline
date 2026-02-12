import logging
import pandas as pd

from project.models import Config
from project.process import (
  process_between_int,
  process_duplicates,
  process_gte_zero,
  process_notna,
  process_chain
)
from project.utils import (
  rename_columns,
  start_main_process,
)

logger = logging.getLogger(__name__)

def process_country(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df["country"].notna()
  df["country"] = df["country"].str.strip().str.title() # maybe title, maybe not
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = "invalid value :: country"
  return df_accepted, df_rejected

def process_year(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  return process_notna(df, "year")

def process_month(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df["month"].notna() & (df["month"].str.strip().str.len() <= 9) # September is longest month name with 9 characters
  df["month"] = df["month"].str.strip().str.title() # yes title
  valid_mask = df["month"].notna()
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = "invalid value :: month"
  return df_accepted, df_rejected

def process_region(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df["region"].notna()
  df["region"] = df["region"].str.strip().str.title() # maybe title, maybe not
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = "invalid value :: region"
  return df_accepted, df_rejected

def process_fires_count(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  return process_gte_zero(df, "fires_count")

def process_burned_area_hectares(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  return process_gte_zero(df, "burned_area_hectares")

def process_cause(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  missing_mask = df["cause"].isna()
  df.loc[missing_mask, "cause"] = df.loc[missing_mask, "cause"] = "Unknown"
  df["cause"] = df["cause"].str.strip()
  df_rejected = df.iloc[0:0].copy()
  df_rejected["reason"] = pd.Series(dtype="string[pyarrow]")
  return df, df_rejected

def process_temperature_celsius(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  return process_notna(df, "temperature_celsius")

def process_humidity_percent(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  return process_between_int(df, "humidity_percent", 0, 100)

def process_wind_speed_kmh(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  return process_gte_zero(df, "wind_speed_kmh")

def transform_data_completely(config: Config, source_index: int, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  logger.info("transforming data")
  df = rename_columns(config, source_index, df)
  result = process_chain(df, (
    process_country,
    process_year,
    process_month,
    process_region,
    process_fires_count,
    process_burned_area_hectares,
    process_cause,
    process_temperature_celsius,
    process_humidity_percent,
    process_wind_speed_kmh,
    process_duplicates
  ))
  logger.info("successfully transformed data")
  return result

def start(): start_main_process("config/wildfire_global.yaml", transform_data_completely)

__all__ = ["start"]
