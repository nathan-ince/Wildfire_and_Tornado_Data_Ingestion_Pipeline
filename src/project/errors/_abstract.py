from project.utils.helpers import format_double_arguments

class AbstractError(Exception):
  def __init__(self, *args: str):
    self.message = " :: ".join(*args)
    super().__init__(self.message)

__all__ = ["AbstractError"]
