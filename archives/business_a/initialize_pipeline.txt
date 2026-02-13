################################################################################################

from logging import getLogger
from sqlalchemy import text

################################################################################################

from project.core import dbengine
from project.errors.abstract import AbstractError
from project.types import InitializePipelineAction, PipelineStatus

################################################################################################

logger = getLogger(__name__)

################################################################################################

INSERT_PIPELINE_WITH_NAME_AND_STATUS = text("INSERT INTO pipeline (name, status) VALUES (:name, :status);")

UPDATE_PIPELINE_BY_NAME_SET_STATUS = text("UPDATE pipeline SET status = :status WHERE name = :name;")

################################################################################################

class InitializePipelineError(AbstractError): pass

################################################################################################

def initialize_pipeline(pipeline_name: str, action: InitializePipelineAction) -> None:
  """
  ### **Throws**

  `InitializePipelineError` - if an error occurs
  """
  try:
    logger.info("initializing pipeline %s", pipeline_name)
    with dbengine.begin() as connection:
      match action:
        case InitializePipelineAction.Update:
          result = connection.execute(UPDATE_PIPELINE_BY_NAME_SET_STATUS, { "name": pipeline_name, "status": PipelineStatus.Running })
          if result.rowcount != 1: raise InitializePipelineError(f"{result.rowcount} rows were updated", f"1 and only 1 row should have been updated")
        case InitializePipelineAction.Insert:
          result = connection.execute(INSERT_PIPELINE_WITH_NAME_AND_STATUS, { "name": pipeline_name, "status": PipelineStatus.Running })
          if result.rowcount != 1: raise InitializePipelineError(f"{result.rowcount} rows were inserted", f"1 and only 1 row should have been inserted")
    logger.info("pipeline %s has been initialized", pipeline_name)
    return
  except InitializePipelineError as e:
    logger.error(e.message)
    raise
  except Exception as e:
    logger.warning("failed to initialize pipeline %s", pipeline_name)
    exception = InitializePipelineError(f"Exception = {type(e).__name__}")
    logger.error(exception.message)
    raise exception from e

################################################################################################

__all__ = ["initialize_pipeline", "InitializePipelineError"]

################################################################################################
