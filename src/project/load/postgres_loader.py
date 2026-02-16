import logging

from pandas import DataFrame
from project.core import get_engine
from project.models import Config

logger = logging.getLogger(__name__)

def load_to_postgres(config: Config, df_accepted: DataFrame, df_rejected: DataFrame):
  if df_accepted.empty is False: # accepted
    logger.info("loading accepted records into postgres", extra={
      "table_name": config.target.tables.accepted,
      "record_count": df_accepted.shape[0],
    })
    df_accepted.to_sql(
      name=config.target.tables.accepted,
      con=get_engine(),
      if_exists="replace",
      index=False,
    )
    logger.info("loaded accepted records into postgres")
  else:
    logger.info("no accepted records to load into postgres")

  if df_rejected.empty is False: # rejected
    logger.info("loading rejected records into postgres", extra={
      "table_name": config.target.tables.rejected,
      "record_count": df_rejected.shape[0],
    })
    df_rejected.to_sql(
      name=config.target.tables.rejected,
      con=get_engine(),
      if_exists="replace",
      index=False,
    )
    logger.info("loaded rejected records into postgres")
  else:
    logger.info("no rejected records to load into postgres")