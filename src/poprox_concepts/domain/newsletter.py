from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from poprox_concepts.domain.article import Article


class Impression(BaseModel):
    newsletter_id: UUID
    position: int
    article: Article
    created_at: datetime | None = None


class Newsletter(BaseModel):
    newsletter_id: UUID = Field(default_factory=uuid4)
    account_id: UUID
    treatment_id: UUID | None = None
    impressions: list[Impression]
    subject: str
    body_html: str
    created_at: datetime | None = None

    def articles(self) -> list[Article]:
        return [impression.article for impression in self.impressions]
