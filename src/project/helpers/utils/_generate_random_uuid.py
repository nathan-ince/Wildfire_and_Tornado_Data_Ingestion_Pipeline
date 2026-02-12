from uuid import uuid4, UUID

def generate_random_uuid() -> UUID:
  return uuid4()

__all__ = ["generate_random_uuid"]
