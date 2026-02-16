# import pandas as pd

# def validate_notna(df: pd.DataFrame, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
#     valid_mask = df[name].notna()
#     df_accepted = df[valid_mask]
#     df_rejected = df[~valid_mask].copy()
#     df_rejected["rejected_reason"] = f"invalid value :: field name = {name}"
#     return df_accepted, df_rejected

import pandas as pd

def validate_notna(df: pd.DataFrame, name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid_mask = df[name].notna()

    # ✅ force pure bool mask
    valid_mask = valid_mask.fillna(False).astype(bool)

    df_accepted = df.loc[valid_mask]
    df_rejected = df.loc[~valid_mask].copy()
    df_rejected["rejected_reason"] = f"invalid value :: field name = {name}"
    return df_accepted, df_rejected
