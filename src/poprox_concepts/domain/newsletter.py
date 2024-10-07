from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from poprox_concepts.domain.article import Article


class Newsletter(BaseModel):
    newsletter_id: UUID = Field(default_factory=uuid4)
    account_id: UUID
    treatment_id: UUID | None = None
    articles: list[Article]
    subject: str
    body_html: str
    created_at: datetime | None = None
