################################################################################################

from logging import getLogger
from uuid import uuid4

################################################################################################

from project.models import PipelineConfigurationSettings as Config

from project.sql import (
  insert_main_process, InsertMainProcessError,
  update_main_process, UpdateMainProcessError
)

from project.utils import generate_timestamp

################################################################################################

from .start_batch_process import start_batch_process

################################################################################################

logger = getLogger(__name__)

################################################################################################

def start_main_process(config: Config) -> None:
  logger.info("starting main process")
  main_process_start_timestamp = generate_timestamp()
  logger.info("main process started at %s", main_process_start_timestamp)
  main_process_id = uuid4()
  logger.debug("main_process_id = %s", main_process_id)
  try: insert_main_process(config.name, main_process_id, main_process_start_timestamp)
  except InsertMainProcessError:
    main_process_final_timestamp = generate_timestamp()
    logger.warning("main process aborted at %s", main_process_final_timestamp)
    return
  source_count = len(config.external.sources)
  logger.debug("source_count = %s", source_count)
  for source_index in range(source_count):
    logger.info("processing source %d of %d", source_index + 1, source_count)
    start_batch_process(config, source_index, main_process_id)
  main_process_final_timestamp = generate_timestamp()
  try: update_main_process(main_process_id, main_process_final_timestamp)
  except UpdateMainProcessError:
    logger.warning("main process aborted at %s", main_process_final_timestamp)
    return
  logger.info("main process completed at %s", main_process_final_timestamp)

################################################################################################

__all__ = ["start_main_process"]

################################################################################################
