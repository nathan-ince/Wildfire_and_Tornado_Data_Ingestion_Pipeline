from pandas import DataFrame

def process_duplicates(data: DataFrame) -> tuple[DataFrame, DataFrame]:
  invalid_mask = data.duplicated(keep=False)
  df_accepted = data[~invalid_mask]
  df_rejected = data[invalid_mask].copy()
  df_rejected["reason"] = "duplicate record"
  return df_accepted, df_rejected

__all__ = ["process_duplicates"]
