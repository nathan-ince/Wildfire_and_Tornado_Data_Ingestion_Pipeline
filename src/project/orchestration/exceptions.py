from project.helpers.errors import AbstractError


class MainProcessError(AbstractError):
    """Raised when the main orchestration process fails."""
    pass


class BatchProcessError(AbstractError):
    """Raised when an individual batch process fails."""
    pass