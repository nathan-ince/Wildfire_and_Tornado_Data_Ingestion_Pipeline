import logging

from enum import Enum

logger = logging.getLogger(__name__)

class AbstractEnum(Enum):

  @classmethod
  def get_value_tuple(cls) -> tuple:
    return tuple(x.value for x in cls)
  
  @classmethod
  def get_value_set(cls) -> set:
    return set(x.value for x in cls)

__all__ = ["AbstractEnum"]
