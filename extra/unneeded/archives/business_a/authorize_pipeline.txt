################################################################################################

from dataclasses import dataclass
from logging import getLogger
from sqlalchemy import text
from typing import Optional, cast

################################################################################################

from project.core import dbengine
from project.models import PipelineConfigurationSettings as Config
from project.types import InitializePipelineAction, PipelineStatus

################################################################################################

logger = getLogger(__name__)

################################################################################################

SELECT_PIPELINE_STATUS_BY_NAME = text("SELECT status FROM pipeline WHERE name = :name;")

################################################################################################

class AuthorizePipelineError(Exception):
  def __init__(self, reason: str = "N/A"):
    self.reason = reason
    self.message = f"authorize pipeline error :: reason = {reason}"
    super().__init__(self.message)

@dataclass
class AuthorizePipelineResult:
  status: Optional[PipelineStatus]
  action: Optional[InitializePipelineAction]

def authorize_pipeline(pipeline_name: str) -> AuthorizePipelineResult:
  """
  ### **Throws**

  `AuthorizePipelineError` - if an error occurs
  """
  try:
    logger.info("authorizing pipeline %s", pipeline_name)
    with dbengine.connect() as connection:
      pipeline_status = cast(Optional[PipelineStatus], connection.execute(SELECT_PIPELINE_STATUS_BY_NAME, { "name": pipeline_name }).scalar_one_or_none())
      match pipeline_status:
        case PipelineStatus.Idle:
          logger.debug("pipeline %s is idle", pipeline_name)
          logger.info("pipeline %s has been authorized", pipeline_name)
          return AuthorizePipelineResult(pipeline_status, InitializePipelineAction.Update)
        case PipelineStatus.Running:
          logger.debug("pipeline %s is running", pipeline_name)
          logger.warning("pipeline %s has been blocked", pipeline_name)
          return AuthorizePipelineResult(pipeline_status, None)
        case None:
          logger.debug("pipeline %s is absent", pipeline_name)
          logger.info("pipeline %s has been authorized", pipeline_name)
          return AuthorizePipelineResult(pipeline_status, InitializePipelineAction.Insert)
  except Exception as e:
    logger.warning("failed to authorize pipeline %s", pipeline_name)
    exception = AuthorizePipelineError(f"Exception = {type(e).__name__}")
    logger.error(exception.message)
    raise exception from e

################################################################################################

__all__ = ["authorize_pipeline", "AuthorizePipelineResult", "AuthorizePipelineError"]

################################################################################################
