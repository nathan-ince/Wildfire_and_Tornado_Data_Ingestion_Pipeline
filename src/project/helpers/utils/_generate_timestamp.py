from datetime import datetime, timezone

def generate_timestamp() -> datetime:
  return datetime.now(timezone.utc)

__all__ = ["generate_timestamp"]
