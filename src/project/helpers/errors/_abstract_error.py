class AbstractError(Exception):
  def __init__(self, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs
    self.message = " :: ".join(args)

__all__ = ["AbstractError"]
