from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from poprox_concepts.domain.article import Article


class RecommenderInfo(BaseModel):
    """
    Identity and versioning metadata for the system that generated the provided
    recommendations.
    """

    name: str | None = None
    version: str | None = None
    hash: str | None = None


class Impression(BaseModel):
    impression_id: UUID | None = Field(default_factory=uuid4)
    newsletter_id: UUID | None = None
    position: int
    article: Article
    created_at: datetime | None = None
    extra: dict[str, Any] | None = None
    headline: str | None = None
    subhead: str | None = None
    preview_image_id: UUID | None = None
    feedback: bool | None = None
    section_name: str | None = None
    position_in_section: int | None = None

    def model_post_init(self, __context):
        """This function is automatically called by the pydantic framework after the model object is initialized."""
        self.headline = self.headline or self.article.headline
        self.subhead = self.subhead or self.article.subhead
        self.preview_image_id = self.preview_image_id or self.article.preview_image_id


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
