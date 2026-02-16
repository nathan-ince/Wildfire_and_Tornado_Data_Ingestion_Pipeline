################################################################################################

import logging

from logging.handlers import RotatingFileHandler

from project.core import settings

################################################################################################

def configure():
  settings.log_directory_path.mkdir(exist_ok=True)

  root_logger = logging.getLogger()
  root_logger.setLevel(logging.DEBUG)

  file_handler = RotatingFileHandler(
    filename=settings.log_directory_path/settings.tests_log_file_name,
    encoding="utf-8",
    maxBytes=5 * 1024 * 1024,
    backupCount=4
  )
  console_handler = logging.StreamHandler()

  file_handler.setLevel(logging.INFO)
  console_handler.setLevel(logging.DEBUG)

  file_formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(module)s:%(lineno)d] [%(levelname)s] %(message)s")
  console_formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(module)s:%(lineno)d] [%(levelname)s] %(message)s")

  file_handler.setFormatter(file_formatter)
  console_handler.setFormatter(console_formatter)

  root_logger.addHandler(file_handler)
  root_logger.addHandler(console_handler)

################################################################################################
