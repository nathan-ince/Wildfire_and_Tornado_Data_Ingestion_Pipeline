import pandas as pd

from typing import Literal

def process_between_int(df: pd.DataFrame, name: str, left: int, right: int, inclusive: Literal["both", "neither", "left", "right"] = "both") -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df[name].notna() & df[name].between(left, right, inclusive)
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = f"invalid value :: {name}"
  return df_accepted, df_rejected

def process_gte_zero(df: pd.DataFrame, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df[name].notna() & df[name].ge(0)
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = f"invalid value :: {name}"
  return df_accepted, df_rejected

def process_latitude(df: pd.DataFrame, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df[name].notna() & df[name].between(-90, 90)
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = f"invalid value :: {name}"
  return df_accepted, df_rejected

def process_longitude(df: pd.DataFrame, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df[name].notna() & df[name].between(-180, 180)
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = f"invalid value :: {name}"
  return df_accepted, df_rejected

__all__ = [
  "process_between_int",
  "process_gte_zero",
  "process_latitude",
  "process_longitude"
]
