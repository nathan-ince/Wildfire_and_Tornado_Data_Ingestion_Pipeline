"""
A special function that returns `tuple[DataFrame, DataFrame]`

This function will accept `DataFrame` and a sequence processes, which are functions that specifically accept `DataFrame` and return `tuple[DataFrame, DataFrame]`.

There are some processes defined in `._process_utils.py`.

The rejected `DataFrame`(s) will be collected in a list until the processes are complete, then combined into one `DataFrame`.
"""

from pandas import DataFrame, concat
from typing import Callable

def process_chain(df: DataFrame, fs: tuple[Callable[[DataFrame], tuple[DataFrame, DataFrame]], ...]) -> tuple[DataFrame, DataFrame]:
  rejected_dfs: list[DataFrame] = []
  df_accepted = df.copy()
  for f in fs:
    df_accepted, df_rejected = f(df_accepted)
    rejected_dfs.append(df_rejected)
  return df_accepted, concat(rejected_dfs)

__all__ = ["process_chain"]
