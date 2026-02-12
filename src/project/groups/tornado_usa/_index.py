import logging
import pandas as pd

from project.core import dbengine
from project.models import Config
from project.process import (
  process_between_int,
  process_gte_zero,
  process_latitude,
  process_longitude,
  process_chain
)
from project.utils import (
  load_config_from_yaml, LoadConfigFromYamlError,
  load_data_with_pandas, LoadDataWithPandasError
)

logger = logging.getLogger(__name__)

NAME = "tornado_usa"
CONFIG_FILE_PATH = "config/tornado_usa.yaml"
KWARGS = { "ingest_name": NAME, "config_file_path": CONFIG_FILE_PATH }
# ATTEMPT_MESSAGE = f"ingesting {NAME}"
# SUCCESS_MESSAGE = f"successfully ingested {NAME}"
# FAILURE_MESSAGE = f"failed to ingest {NAME}"

def process_year(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df["year"].notna()
  recovery_mask = ~valid_mask & df["date"].notna()
  recovery_dates = df.loc[recovery_mask, "date"].astype("date32[pyarrow]") # It should already be this type but the type checker doesn't know that.
  df.loc[recovery_mask, "year"] = recovery_dates.dt.year.astype("int16[pyarrow]")
  valid_mask = df["year"].notna()
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = "invalid value :: year"
  return df_accepted, df_rejected

def process_month(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df["month"].notna() & df["month"].between(1, 12)
  recovery_mask = ~valid_mask & df["date"].notna()
  recovery_dates = df.loc[recovery_mask, "date"].astype("date32[pyarrow]") # It should already be this type but the type checker doesn't know that.
  df.loc[recovery_mask, "month"] = recovery_dates.dt.month.astype("int16[pyarrow]")
  valid_mask = df["month"].notna()
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = "invalid value :: month"
  return df_accepted, df_rejected

def process_day(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df["day"].notna() & df["day"].between(1, 31)
  recovery_mask = ~valid_mask & df["date"].notna()
  recovery_dates = df.loc[recovery_mask, "date"].astype("date32[pyarrow]") # It should already be this type but the type checker doesn't know that.
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

def process_state(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df["state"].notna() & (df["state"].str.strip().str.len() == 2)
  df.loc[valid_mask, "state"] = df.loc[valid_mask, "state"].str.strip().str.upper()
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = "invalid value :: state"
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

def process_year_month_day_date(df: pd.DataFrame):
  valid_mask = df["year"].notna() & df["month"].notna() & df["day"].notna() & df["date"].notna()
  df_accepted = df.loc[valid_mask]
  df_rejected = df.loc[~valid_mask]
  df_rejected["reason"] = "invalid combination of values :: year, month, or day is N/A :: date is N/A"
  return df_accepted, df_rejected

def dedupe(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  invalid_mask = data.duplicated(keep=False)
  df_accepted = data[~invalid_mask]
  df_rejected = data[invalid_mask].copy()
  df_rejected["reason"] = "duplicate record"
  return df_accepted, df_rejected

def transform_data_completely(config: Config, source_index: int, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  source = config.sources[source_index]
  df = df[list(source.mapping.keys())].rename(columns={mapping[0]: mapping[1].name for mapping in source.mapping.items()})
  return process_chain(df, (
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
    process_year_month_day_date,
    dedupe
  ))

def store_data_in_postgres(config: Config, df_accepted: pd.DataFrame, df_rejected: pd.DataFrame):
  if df_accepted.empty is False: # accepted
    df_accepted.to_sql(
      name=config.target.tables.accepted,
      con=dbengine,
      if_exists="delete_rows",
      index=False
    )
  if df_rejected.empty is False: # rejected
    df_rejected.to_sql(
      name=config.target.tables.rejected,
      con=dbengine,
      if_exists="delete_rows",
      index=False
    )

def run():
  logger.info("starting pipeline", extra=KWARGS)
  config = load_config_from_yaml(CONFIG_FILE_PATH)
  for source_index in range(len(config.sources)):
    logger.debug("processing source %s/%s", source_index + 1, len(config.sources))
    df_raw = load_data_with_pandas(config, source_index)
    df_accepted, df_rejected = transform_data_completely(config, source_index, df_raw)
    store_data_in_postgres(config, df_accepted, df_rejected)

__all__ = ["run"]
