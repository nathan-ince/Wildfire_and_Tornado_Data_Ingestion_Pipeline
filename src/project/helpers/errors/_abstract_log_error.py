from logging import Logger

from ._abstract_error import AbstractError

class AbstractLogError(Exception):
  def __init__(self, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs
    self.message = " :: ".join(args)

__all__ = ["AbstractLogError"]
