import pandas as pd

def validate_latitude(df: pd.DataFrame, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_mask = (
        df[name].notna()
        & df[name].between(-90, 90).fillna(False)
    )
    df_accepted = df[valid_mask]
    df_rejected = df[~valid_mask].copy()
    df_rejected["rejected_reason"] = f"invalid value :: field name = {name}"
    return df_accepted, df_rejected


def validate_longitude(df: pd.DataFrame, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_mask = (
        df[name].notna()
        & df[name].between(-180, 180).fillna(False)
    )
    df_accepted = df[valid_mask]
    df_rejected = df[~valid_mask].copy()
    df_rejected["rejected_reason"] = f"invalid value :: field name = {name}"
    return df_accepted, df_rejected