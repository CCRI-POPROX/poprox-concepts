from uuid import UUID

from pydantic import BaseModel


class Tracking_Link_Data(BaseModel):
    newsletter_id: UUID
    account_id: UUID
    url: str
    article_id: UUID


class Unsubscribe_Link_Data(BaseModel):
    account_id: UUID
    newsletter_id: UUID = None
