import pandas as pd

def validate_string_max_length(df: pd.DataFrame, name: str, n: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    s = df[name].astype("string") 
    s = s.str.strip()
    length = s.str.len()

    valid_mask = (length.notna() & (length > 0) & (length <= n)).fillna(False)

    df_accepted = df[valid_mask]
    df_rejected = df[~valid_mask].copy()
    df_rejected["rejected_reason"] = f"invalid value :: field name = {name}"
    return df_accepted, df_rejected


def validate_string_exact_length(df: pd.DataFrame, name: str, n: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    s = df[name].astype("string")
    s = s.str.strip()
    length = s.str.len()

    valid_mask = (length.notna() & (length == n) & (length > 0)).fillna(False)

    df_accepted = df[valid_mask]
    df_rejected = df[~valid_mask].copy()
    df_rejected["rejected_reason"] = f"invalid value :: field name = {name}"
    return df_accepted, df_rejected