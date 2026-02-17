from uuid import UUID
from datetime import datetime, timezone

from project.helpers.utils import generate_random_uuid, generate_timestamp


def test_generate_random_uuid():
    value = generate_random_uuid()
    assert isinstance(value, UUID)


def test_generate_timestamp():
    time_stamp = generate_timestamp()
    assert isinstance(time_stamp, datetime)
    assert time_stamp.tzinfo is timezone.utc