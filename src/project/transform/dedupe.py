import pandas as pd

def dedupe_keep_first(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
  invalid_mask = data.duplicated(keep="first")
  df_accepted = data[~invalid_mask]
  df_rejected = data[invalid_mask].copy()
  df_rejected["reason"] = "duplicate record"
  return df_accepted, df_rejected