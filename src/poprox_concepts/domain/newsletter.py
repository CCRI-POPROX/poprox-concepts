from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from poprox_concepts.api.recommendations import RecommenderInfo
from poprox_concepts.domain.article import Article


class Impression(BaseModel):
    impression_id: UUID = Field(default_factory=uuid4)
    newsletter_id: UUID | None
    position: int
    article: Article
    created_at: datetime | None = None
    extra: dict[str, Any] | None = None
    headline: str | None = None
    subhead: str | None = None
    feedback: bool | None = None
    section_name: str | None = None
    position_in_section: int | None = None


class Newsletter(BaseModel):
    newsletter_id: UUID = Field(default_factory=uuid4)
    account_id: UUID
    treatment_id: UUID | None = None
    experience_id: UUID | None = None
    impressions: list[Impression]
    subject: str
    body_html: str
    created_at: datetime | None = None
    recommender_info: RecommenderInfo | None = None
    feedback: str | None = None

    @property
    def articles(self) -> list[Article]:
        return [impression.article for impression in self.impressions]
