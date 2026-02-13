################################################################################################

from logging import getLogger
from sqlalchemy import text

################################################################################################

from project.core import dbengine
from project.errors.abstract import AbstractError
from project.types import PipelineStatus

################################################################################################

logger = getLogger(__name__)

################################################################################################

UPDATE_PIPELINE_BY_NAME_SET_STATUS = text("UPDATE pipeline SET status = :status WHERE name = :name;")

################################################################################################

class FinalizePipelineError(AbstractError): pass

################################################################################################

def finalize_pipeline(pipeline_name: str) -> None:
  """
  ### **Throws**

  `FinalizePipelineError` - if an error occurs
  """
  try:
    logger.info("finalizing pipeline %s", pipeline_name)
    with dbengine.begin() as connection:
      result = connection.execute(UPDATE_PIPELINE_BY_NAME_SET_STATUS, { "name": pipeline_name, "status": PipelineStatus.Idle })
      if result.rowcount != 1: raise FinalizePipelineError(f"{result.rowcount} rows were affected", f"1 and only 1 row should have been affected")
    logger.info("pipeline %s has been finalized", pipeline_name)
  except FinalizePipelineError as e:
    logger.error(e.message)
    raise
  except Exception as e:
    logger.warning("failed to finalize pipeline %s", pipeline_name)
    exception = FinalizePipelineError(f"Exception = {type(e).__name__}")
    logger.error(exception.message)
    raise exception from e

################################################################################################

__all__ = ["finalize_pipeline", "FinalizePipelineError"]

################################################################################################
