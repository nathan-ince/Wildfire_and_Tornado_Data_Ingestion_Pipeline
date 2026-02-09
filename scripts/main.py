import logging

# from project.business.models.config import Config
# from project.business.utils import load_config_from_yaml

from project.core import configure_logging
from project.business.utils import load_content_from_yaml
from typing import Any

from project.helpers.enums import PostgresDataType
from project.helpers.utils import verify_set, verify_dict, verify_list, verify_tuple

CONFIG_FILE_PATH = "config/tornado_usa.aml"

if __name__ == "__main__":
  configure_logging()
  # verify_set({True, False, 8}, verify_elements=True, elements_target_type=(str, int))
  # PostgresDataType.assign("bigint")
  verify_list([1, 2, 3, True, "hello", "[1, 2, 3]"], verify_elements=True, elements_target_type=(str, int), track_entity_value=True, track_entity_source_type=False, track_entity_target_type=False, track_element_value=True, track_element_source_type=True, track_element_target_type=True)
  load_content_from_yaml(CONFIG_FILE_PATH)
