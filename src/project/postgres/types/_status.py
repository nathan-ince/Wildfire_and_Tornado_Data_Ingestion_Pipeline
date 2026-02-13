from project.helpers.enums import AbstractStringEnum

class Status(AbstractStringEnum):
  Running = "running"
  Success = "success"
  Warning = "warning"
  Failure = "failure"

__all__ = ["Status"]
