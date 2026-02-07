import logging
from uuid import uuid4, UUID

from project.errors import AbstractError
from project.models import Config
from project.utils.helpers import generate_timestamp
from project.utils.load import (
  load_config_from_yaml, LoadConfigFromYamlError,
  load_data_from_source, LoadDataFromSourceError
)

from project.utils.clean import clean_tornado_usa
from project.utils.dedupe import dedupe_tornado
from project.utils.validate import validate_tornado_usa

logger = logging.getLogger(__name__)

CONFIG_FILE_PATH = "config/tornado_usa.yaml"

class PipelineError(AbstractError): pass

def pipeline():
  main_process_key = uuid4()
  try: config = load_config_from_yaml(CONFIG_FILE_PATH)
  except LoadConfigFromYamlError as e:
    error = PipelineError("pipeline error", e.message)
    logger.error(error.message, extra={"main_process_key": main_process_key, "config_path": CONFIG_FILE_PATH})
    raise error from e
  source_count = len(config.sources)
  for source_index in range(source_count):
    source = config.sources[source_index]
    source_format = source.format
    source_path = source.path
    try: raw = load_data_from_source(source_format, source_path)
    except LoadDataFromSourceError as e:
      error = PipelineError("pipeline error", e.message)
      logger.error(error.message, extra={"main_process_key": main_process_key, "config_path": CONFIG_FILE_PATH, "source_index": source_index, "source_format": source_format, "source_path": source_path})
      raise error from e
    try: 
    renamed = raw[list(source.columns.keys())].rename(columns=source.columns)
