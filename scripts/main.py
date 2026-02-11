import logging

# from project.business.models.config import Config
# from project.business.utils import load_config_from_yaml

from project.core import configure_logging

from project.domain.ingest import tornado_usa
from project.domain.utils import load_config_from_yaml
from project.helpers.enums import PostgresDataType

logger = logging.getLogger(__name__)

CONFIG_FILE_PATH = "config/tornado_usa.yaml"

if __name__ == "__main__":
  configure_logging()
  tornado_usa.ingest()
