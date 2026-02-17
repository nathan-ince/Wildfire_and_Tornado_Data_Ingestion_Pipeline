import logging

from pandas import DataFrame

from project.core import get_settings, get_engine
from project.helpers.errors import AbstractError
from project.read.read_sql import read_sql_statement

from sqlalchemy import UUID

class LoadAcceptedStageError(AbstractError): pass
class LoadRejectedStageError(AbstractError): pass
class MergeFinalError(AbstractError): pass

def buildNoDataMessage(name: str) -> str:
  return f"no data to load into {name}"

def buildLoadStartMessage(name: str) -> str:
  return f"loading data into {name}"

def buildLoadSuccessMessage(name: str) -> str:
  return f"successfully loaded data into {name}"

def buildLoadFailureMessage(name: str) -> str:
  return f"failed to load data into {name}"

ACCEPTED_STAGE_NAME = "accepted stage"
REJECTED_STAGE_NAME = "rejected stage"

logger = logging.getLogger(__name__)

def load_into_accepted_stage(table_name: str, data: DataFrame) -> None:
  """
  ### **Returns**

  `None`

  ---

  ### **Throws**

  `LoadAcceptedStageError`
  """
  kwargs = { "table_name": table_name, "record_count": data.shape[0] }
  if data.empty is True:
    logger.info(buildNoDataMessage(ACCEPTED_STAGE_NAME), extra=kwargs)
    return None
  try:
    logger.info(buildLoadStartMessage(ACCEPTED_STAGE_NAME), extra=kwargs)
    data.to_sql(table_name, get_engine(), if_exists="replace", index=False, dtype={"batch_process_id": UUID})
    logger.info(buildLoadSuccessMessage(ACCEPTED_STAGE_NAME))
  except Exception as e:
    error = LoadAcceptedStageError(buildLoadFailureMessage(ACCEPTED_STAGE_NAME), cause=type(e).__name__, **kwargs)
    logger.error(error.message, extra=error.kwargs)
    raise error from e

def load_into_rejected_stage(table_name: str, data: DataFrame) -> None:
  """
  ### **Returns**

  `None`

  ---

  ### **Throws**

  `LoadRejectedStageError`
  """
  kwargs = { "table_name": table_name, "record_count": data.shape[0] }
  if data.empty is True:
    logger.info(buildNoDataMessage(REJECTED_STAGE_NAME), extra=kwargs)
    return None
  try:
    logger.info(buildLoadStartMessage(REJECTED_STAGE_NAME), extra=kwargs)
    data.astype("string[pyarrow]").to_sql(table_name, get_engine(), if_exists="replace", index=False, dtype={"batch_process_id": UUID})
    logger.info(buildLoadSuccessMessage(REJECTED_STAGE_NAME))
  except Exception as e:
    error = LoadRejectedStageError(buildLoadFailureMessage(REJECTED_STAGE_NAME), cause=type(e).__name__, **kwargs)
    logger.error(error.message, extra=error.kwargs)
    raise error from e

def merge_stage_into_final(merge_stmt_path: str, stage_table_name: str | None = None, final_table_name: str | None = None):
  kwargs = { "stage_table_name": stage_table_name, "final_table_name": final_table_name }
  try:
    with get_engine().begin() as connection:
      stmt = read_sql_statement(merge_stmt_path)
      logger.info("merging stage table into final table", extra=kwargs)
      connection.execute(stmt)
      logger.info("successfully merged stage table into final table", extra=kwargs)
  except Exception as e:
    print(e)
    error = MergeFinalError("failed to merge stage table into final table", cause=type(e).__name__, **kwargs)
    logger.error(error.message, extra=error.kwargs)
    raise error from e
