from uuid import UUID
from datetime import datetime, timezone

from project.helpers.utils import generate_random_uuid, generate_timestamp


def test_generate_random_uuid_returns_uuid():
    value = generate_random_uuid()
    assert isinstance(value, UUID)


def test_generate_timestamp_returns_utc_datetime():
    ts = generate_timestamp()
    assert isinstance(ts, datetime)
    assert ts.tzinfo is timezone.utc