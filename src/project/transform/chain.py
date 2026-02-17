from pandas import DataFrame, concat
from typing import Callable

def validate_chain(df: DataFrame, fs: tuple[Callable[[DataFrame], tuple[DataFrame, DataFrame]], ...]) -> tuple[DataFrame, DataFrame]:
  rejected_dfs: list[DataFrame] = []
  df_accepted = df.copy()
  for f in fs:
    df_accepted, df_rejected = f(df_accepted)
    rejected_dfs.append(df_rejected)
  return df_accepted, concat(rejected_dfs)
