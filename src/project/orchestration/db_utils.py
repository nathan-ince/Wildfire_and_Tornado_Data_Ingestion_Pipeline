import logging

from datetime import datetime
from uuid import UUID

from project.core.db import get_engine
from project.helpers.errors import AbstractError
from project.orchestration.types import Status
from project.io.sql_reader import read_sql_statement

INITIALIZE_MAIN_PROCESS = read_sql_statement("initialize_main_process.sql")
INITIALIZE_BATCH_PROCESS = read_sql_statement("initialize_batch_process.sql")
FINALIZE_MAIN_PROCESS = read_sql_statement("finalize_main_process.sql")
FINALIZE_BATCH_PROCESS = read_sql_statement("finalize_batch_process.sql")

class InitializeMainProcessError(AbstractError): pass
class InitializeBatchProcessError(AbstractError): pass
class FinalizeMainProcessError(AbstractError): pass
class FinalizeBatchProcessError(AbstractError): pass

logger = logging.getLogger(__name__)

def initialize_main_process(main_process_id: UUID, main_process_start_timestamp: datetime) -> None:
  try:
    logger.info("initializing main process", extra={
      "main_process_id": str(main_process_id),
      "main_process_start_timestamp": str(main_process_start_timestamp)
    })
    with get_engine().begin() as connection:
      connection.execute(INITIALIZE_MAIN_PROCESS, {
        "id": main_process_id,
        "status": Status.Running.value,
        "start_timestamp": main_process_start_timestamp
      })
    logger.info("initialized main process", extra={
      "main_process_id": str(main_process_id),
      "main_process_start_timestamp": str(main_process_start_timestamp)
    })
  except Exception as err:
    print(err)
    error = InitializeMainProcessError(
      "failed to initialize main process",
      main_process_id=str(main_process_id),
      main_process_start_timestamp=str(main_process_start_timestamp)
    )
    logger.error(error.message, extra=error.kwargs)
    raise error from err

def initialize_batch_process(main_process_id: UUID, batch_process_id: UUID, batch_process_start_timestamp: datetime) -> None:
  try:
    logger.info("initializing batch process", extra={
      "main_process_id": str(main_process_id),
      "batch_process_id": str(batch_process_id),
      "batch_process_start_timestamp": str(batch_process_start_timestamp)
    })
    with get_engine().begin() as connection:
      connection.execute(INITIALIZE_BATCH_PROCESS, {
        "main_process_id": main_process_id,
        "id": batch_process_id,
        "status": Status.Running.value,
        "start_timestamp": batch_process_start_timestamp
      })
    logger.info("initialized batch process", extra={
      "main_process_id": str(main_process_id),
      "batch_process_id": str(batch_process_id),
      "batch_process_start_timestamp": str(batch_process_start_timestamp)
    })
  except Exception as err:
    error = InitializeBatchProcessError(
      "failed to initialize batch process",
      main_process_id=str(main_process_id),
      batch_process_id=str(batch_process_id),
      batch_process_start_timestamp=str(batch_process_start_timestamp)
    )
    logger.error(error.message, extra=error.kwargs)
    raise error from err

def finalize_main_process(main_process_id: UUID, main_process_status: Status, main_process_final_timestamp: datetime) -> None:
  try:
    logger.info("finalizing main process", extra={
      "main_process_id": str(main_process_id),
      "main_process_final_timestamp": str(main_process_final_timestamp)
    })
    with get_engine().begin() as connection:
      connection.execute(FINALIZE_MAIN_PROCESS, {
        "id": main_process_id,
        "status": main_process_status.value,
        "final_timestamp": main_process_final_timestamp
      })
    logger.info("finalized main process", extra={
      "main_process_id": str(main_process_id),
      "main_process_final_timestamp": str(main_process_final_timestamp)
    })
  except Exception as err:
    error = FinalizeMainProcessError(
      "failed to finalize main process",
      main_process_id=str(main_process_id),
      main_process_status=main_process_status.value,
      main_process_final_timestamp=str(main_process_final_timestamp)
    )
    logger.error(error.message, extra=error.kwargs)
    raise error from err

def finalize_batch_process(batch_process_id: UUID, batch_process_status: Status, batch_process_final_timestamp: datetime) -> None:
  try:
    logger.info("finalizing batch process", extra={
      "batch_process_id": str(batch_process_id),
      "batch_process_final_timestamp": str(batch_process_final_timestamp)
    })
    with get_engine().begin() as connection:
      connection.execute(FINALIZE_BATCH_PROCESS, {
        "id": batch_process_id,
        "status": batch_process_status.value,
        "final_timestamp": batch_process_final_timestamp
      })
    logger.info("finalized batch process", extra={
      "batch_process_id": str(batch_process_id),
      "batch_process_final_timestamp": str(batch_process_final_timestamp)
    })
  except Exception as err:
    error = FinalizeBatchProcessError(
      "failed to finalize batch process",
      batch_process_id=str(batch_process_id),
      batch_process_status=batch_process_status.value,
      batch_process_final_timestamp=str(batch_process_final_timestamp)
    )
    logger.error(error.message, extra=error.kwargs)
    raise error from err
