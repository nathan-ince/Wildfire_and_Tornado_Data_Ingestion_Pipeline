import logging
import structlog

from logging.handlers import RotatingFileHandler
from ._env import settings

def configure_logging():
  settings.log_directory_path.mkdir(exist_ok=True)

  root_logger = logging.getLogger()
  root_logger.setLevel(logging.DEBUG)
  root_logger.handlers.clear()

  file_handler = RotatingFileHandler(
    filename=settings.log_directory_path/settings.app_log_file_name,
    encoding="utf-8",
    maxBytes=(5 * 1024 * 1024),
    backupCount=4
  )
  console_handler = logging.StreamHandler()

  file_handler.setLevel(logging.DEBUG)
  console_handler.setLevel(logging.INFO)

  # file_formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(module)s:%(lineno)d] [%(levelname)s] %(message)s")
  # console_formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(module)s:%(lineno)d] [%(levelname)s] %(message)s")

  shared_processors = [
    structlog.processors.TimeStamper("iso", True),
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.ExtraAdder()
  ]

  file_formatter = structlog.stdlib.ProcessorFormatter(
    processor=structlog.processors.JSONRenderer(),
    foreign_pre_chain=shared_processors
  )

  console_formatter = structlog.stdlib.ProcessorFormatter(
    processor=structlog.dev.ConsoleRenderer(
      colors=True,
      pad_level=False,
      pad_event=0
    ),
    foreign_pre_chain=shared_processors
  )

  file_handler.setFormatter(file_formatter)
  console_handler.setFormatter(console_formatter)

  root_logger.addHandler(file_handler)
  root_logger.addHandler(console_handler)

  structlog.configure(
    processors=[
      structlog.stdlib.add_logger_name,
      structlog.stdlib.add_log_level,
      structlog.contextvars.merge_contextvars,
      structlog.processors.format_exc_info,
      structlog.processors.StackInfoRenderer(),
      structlog.stdlib.ProcessorFormatter.wrap_for_formatter
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True
  )

__all__ = ["configure_logging"]
