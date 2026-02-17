import hashlib
import json
import logging
import pandas as pd

from typing import cast

logger = logging.getLogger(__name__)

# not being used
def compute_record_hash_series_include(df: pd.DataFrame, included_fields: list[str]):
  if df.empty is True: return pd.Series([], dtype="string[pyarrow]")
  df_subset = df[included_fields]
  df_subset = df_subset.sort_index(axis=1)
  df_string = df_subset.astype("string[pyarrow]")
  d1_string = df_string.aggregate("|".join, axis=1)
  return d1_string.map(lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest()) # x should be str

def compute_record_hash_series_exclude(df: pd.DataFrame, excluded_fields: list[str] | None = None):
  if df.empty is True: return pd.Series([], dtype="string[pyarrow]")
  if excluded_fields is None: excluded_fields = [] # this because a mutable default is bad (setting default as [] vs None in signature)
  included_fields = [field for field in df.columns if field not in excluded_fields]
  df_subset = df[included_fields]
  df_subset = df_subset.sort_index(axis=1)
  df_string = df_subset.astype("string[pyarrow]")
  d1_string = df_string.aggregate("|".join, axis=1)
  return d1_string.map(lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest()) # x shold be str
