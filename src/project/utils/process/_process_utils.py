"""
All functions that accept `DataFrame` and `str` (field name) and return `tuple[DataFrame, DataFrame]`

The first `DataFrame` contains the accepted records after processing.

The second `DataFrame` contains the rejected records after processing.
"""

import pandas as pd

from typing import Literal

def process_between_int(df: pd.DataFrame, name: str, left: int, right: int, inclusive: Literal["both", "neither", "left", "right"] = "both") -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df[name].notna() & df[name].between(left, right, inclusive)
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = f"invalid value :: field name = {name}"
  return df_accepted, df_rejected

def process_duplicates(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  invalid_mask = data.duplicated(keep=False)
  df_accepted = data[~invalid_mask]
  df_rejected = data[invalid_mask].copy()
  df_rejected["reason"] = "duplicate record"
  return df_accepted, df_rejected

def process_gte_zero(df: pd.DataFrame, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df[name].notna() & df[name].ge(0)
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = f"invalid value :: field name = {name}"
  return df_accepted, df_rejected

def process_latitude(df: pd.DataFrame, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df[name].notna() & df[name].between(-90, 90)
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = f"invalid value :: field name = {name}"
  return df_accepted, df_rejected

def process_longitude(df: pd.DataFrame, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df[name].notna() & df[name].between(-180, 180)
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = f"invalid value :: field name = {name}"
  return df_accepted, df_rejected

def process_notna(df: pd.DataFrame, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df[name].notna()
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = f"invalid value :: field name = {name}"
  return df_accepted, df_rejected

def process_string_notna_at_most_n_characters(df: pd.DataFrame, name: str, n: int) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df[name].notna() & (df[name].str.strip().str.len() <= n)
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = f"invalid value :: field name = {name}"
  return df_accepted, df_rejected

def process_string_notna_exactly_n_characters(df: pd.DataFrame, name: str, n: int) -> tuple[pd.DataFrame, pd.DataFrame]:
  valid_mask = df[name].notna() & (df[name].str.strip().str.len() == n)
  df_accepted = df[valid_mask]
  df_rejected = df[~valid_mask].copy()
  df_rejected["reason"] = f"invalid value :: field name = {name}"
  return df_accepted, df_rejected

__all__ = [
  "process_between_int",
  "process_duplicates",
  "process_gte_zero",
  "process_latitude",
  "process_longitude",
  "process_notna",
  "process_string_notna_at_most_n_characters",
  "process_string_notna_exactly_n_characters"
]
