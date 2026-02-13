from uuid import uuid4, UUID
from datetime import datetime, timezone

def generate_random_uuid() -> UUID:
    return uuid4()

def generate_timestamp() -> datetime:
    return datetime.now(timezone.utc)