from project.helpers.abstract_string_enum import AbstractStringEnum

class Status(AbstractStringEnum):
    Running = "running"
    Success = "success"
    Warning = "warning"
    Failure = "failure"

__all__ = ["Status"]