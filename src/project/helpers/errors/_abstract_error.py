class AbstractError(Exception):
  def __init__(self, *args, error: None = None, **kwargs):
    self.args = args
    self.kwargs = {"error": self.__class__.__name__, **kwargs}
    self.message = " :: ".join(map(str, args))

__all__ = ["AbstractError"]
