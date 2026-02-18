################################################################################################

import numpy as np
import pandas as pd
import pandera.pandas as pa

from pandera import Check, Column, DataFrameSchema

################################################################################################

def not_na(s: pd.Series) -> pd.Series:
  return s.notna()

################################################################################################

schema = DataFrameSchema(
  columns={
    "transaction_id": Column(
      dtype=pa.String,
      checks=[Check.str_startswith("TXN_")],
      nullable=False,
      unique=True
    ),
    "customer_id": Column(
      dtype=pa.String,
      checks=[Check.str_startswith("CUST_")],
      nullable=False
    ),
    "category": Column(
      dtype=pa.String,
      nullable=False
    ),
    "item": Column(
      dtype=pa.String,
      checks=[
        Check.str_startswith("Item_")
      ],
      nullable=False
    ),
    "price_per_unit": Column(
      dtype=pa.Float64,
      checks=[
        Check.greater_than(0.0, error="cannot be negative")
      ],
      nullable=False
    ),
    "quantity": Column(
      dtype=pa.Float64,
      checks=[
        Check.greater_than(0.0, error="cannot be negative")],
      nullable=False
    ),
    "total_spent": Column(
      dtype=pa.Float64,
      checks=[
        Check.greater_than(0.0, error="cannot be negative"),
      ],
      nullable=False
    ),
    "payment_method": Column(
      dtype=pa.String,
      checks=[Check.isin({"Digital Wallet", "Credit Card", "Cash"})],
      nullable=False
    ),
    "location": Column(
      dtype=pa.String,
      checks=Check.isin({"Online", "In-store"}),
      nullable=False
    ),
    "transaction_date": Column(
      dtype=pa.DateTime,
      nullable=False
    ),
    "discount_applied": Column(
      dtype=pa.Bool,
      nullable=False
    )
  },
  checks=[
    Check(lambda df: np.isclose(df["total_spent"], df["price_per_unit"] * df["quantity"]), error="total spent must equal quantity times price per unit"),
    Check(lambda df: ~((df["payment_method"] == "Cash") & (df["location"] == "Online")), error="cannot pay with cash online"),
    Check(lambda df: df["transaction_date"] <= pd.Timestamp.now(), error="transaction date cannot be in the future")
  ],
  coerce=True,
  strict=True
)

################################################################################################

__all__ = ["schema"]

################################################################################################
