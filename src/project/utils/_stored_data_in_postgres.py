import logging

from pandas import DataFrame
from project.core import dbengine
from project.models import Config

logger = logging.getLogger(__name__)

def store_data_in_postgres(config: Config, df_accepted: DataFrame, df_rejected: DataFrame):
  if df_accepted.empty is False: # accepted
    logger.info("storing accepted records in postgres", extra={
      "table_name": config.target.tables.accepted,
      "record_count": df_accepted.shape[0],
    })
    df_accepted.to_sql(
      name=config.target.tables.accepted,
      con=dbengine,
      if_exists="delete_rows",
      index=False,
    )
    logger.info("successfully stored accepted records in postgres")
  else:
    logger.info("no accepted records to store in postgres")

  if df_rejected.empty is False: # rejected
    logger.info("storing rejected records in postgres", extra={
      "table_name": config.target.tables.rejected,
      "record_count": df_rejected.shape[0],
    })
    df_rejected.to_sql(
      name=config.target.tables.rejected,
      con=dbengine,
      if_exists="delete_rows",
      index=False,
    )
    logger.info("successfully stored rejected records in postgres")
  else:
    logger.info("no rejected records to load in postgres")

__all__ = ["store_data_in_postgres"]
