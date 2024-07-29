import base64
import uuid

import pytest

from poprox_concepts.internals import (
    TrackingLinkData,
    from_hashed_base64,
    to_hashed_base64,
)


def test_encode_decode():
    key = "thisisanexamplekey"
    data = TrackingLinkData(
        newsletter_id=uuid.uuid4(),
        account_id=uuid.uuid4(),
        article_id=uuid.uuid4(),
        url="https://test.com",
    )
    encoded = to_hashed_base64(data, key)
    decoded = from_hashed_base64(encoded, key, TrackingLinkData)
    assert decoded == data


def test_without_hmac():
    key = "thisisanexamplekey"
    data = TrackingLinkData(
        newsletter_id=uuid.uuid4(),
        account_id=uuid.uuid4(),
        article_id=uuid.uuid4(),
        url="https://test.com",
    )
    encoded = base64.urlsafe_b64encode(data.model_dump_json().encode("UTF-8")).decode("UTF8")
    with pytest.raises(ValueError):
        from_hashed_base64(encoded, key, TrackingLinkData)


def test_wrong_hmac():
    key = "thisisanexamplekey"
    data = TrackingLinkData(
        newsletter_id=uuid.uuid4(),
        account_id=uuid.uuid4(),
        article_id=uuid.uuid4(),
        url="https://test.com",
    )
    encoded = to_hashed_base64(data, "thisisthewrongkey")
    with pytest.raises(ValueError):
        from_hashed_base64(encoded, key, TrackingLinkData)


def test_invalid_data_fails():
    key = "thisisanexamplekey"
    with pytest.raises(ValueError):
        from_hashed_base64("blah", key, TrackingLinkData)


def test_empty_string_fails():
    key = "thisisanexamplekey"
    with pytest.raises(ValueError):
        from_hashed_base64("", key, TrackingLinkData)
