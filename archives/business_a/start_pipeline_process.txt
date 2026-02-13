################################################################################################

from logging import getLogger

################################################################################################

from .load_configuration import load_configuration, LoadConfigurationError
from .authorize_pipeline import authorize_pipeline, AuthorizePipelineError
from .initialize_pipeline import initialize_pipeline, InitializePipelineError
from .finalize_pipeline import finalize_pipeline, FinalizePipelineError

from .start_main_process import start_main_process

################################################################################################

logger = getLogger()

################################################################################################

def start_pipeline_process():
  logger.info("starting pipeline process")
  try: config = load_configuration()
  except LoadConfigurationError:
    logger.warning("pipeline process aborted")
    raise
  try: result = authorize_pipeline(config.name)
  except AuthorizePipelineError:
    logger.warning("pipeline process aborted")
    raise
  if result.action is None:
    logger.warning("pipeline is running elsewhere :: process aborted")
    return
  try: initialize_pipeline(config.name, result.action)
  except InitializePipelineError:
    logger.warning("pipeline process aborted")
    raise
  start_main_process(config)
  try: finalize_pipeline(config.name)
  except FinalizePipelineError:
    logger.warning("pipeline process aborted")
    raise
  logger.info("pipeline process has been completed")

################################################################################################

__all__ = ["start_pipeline_process"]

################################################################################################
