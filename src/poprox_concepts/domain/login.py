from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class WebLogin(BaseModel):
    account_id: UUID
    newsletter_id: UUID | None = None
    endpoint: str
    created_at: datetime
