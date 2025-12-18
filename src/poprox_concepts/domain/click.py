from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Click(BaseModel):
    article_id: UUID
    newsletter_id: UUID | None = None
    impression_id: UUID | None = None
    timestamp: datetime | None = None
