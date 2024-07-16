import base64
import hashlib
import hmac
from uuid import UUID

from pydantic import BaseModel


class TrackingLinkData(BaseModel):
    newsletter_id: UUID
    account_id: UUID
    url: str
    article_id: UUID


Tracking_Link_Data = TrackingLinkData  # XXX - rename class.


class UnsubscribeLinkData(BaseModel):
    account_id: UUID
    newsletter_id: UUID = None


Unsubscribe_Link_Data = UnsubscribeLinkData  # XXX - rename class.


def to_hashed_base64(data: BaseModel, key: str) -> str:
    raw_data = data.model_dump_json().encode("UTF-8")
    raw_signature = hmac.digest(key.encode("UTF-8"), raw_data, hashlib.sha256)
    b64_data = base64.urlsafe_b64encode(raw_data).decode("UTF-8")
    b64_signature = base64.urlsafe_b64encode(raw_signature).decode("UTF-8")
    return b64_data + "." + b64_signature


def from_hashed_base64(raw: str, key: str, model: type[BaseModel]) -> BaseModel | None:
    if "." not in raw:
        msg = "data could not be parsed"
        raise ValueError(msg)
    else:
        b64_data, b64_signature = raw.split(".", 1)
        raw_data = base64.urlsafe_b64decode(b64_data.encode("utf-8"))
        raw_signature = base64.urlsafe_b64decode(b64_signature.encode("utf-8"))
        expected_signature = hmac.digest(key.encode("UTF-8"), raw_data, hashlib.sha256)
        if hmac.compare_digest(raw_signature, expected_signature):
            return model.model_validate_json(raw_data.decode("utf-8"))
        else:
            msg = "invalid hmac signature"
            raise ValueError(msg)
