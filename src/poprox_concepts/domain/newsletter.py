from datetime import datetime
from itertools import zip_longest
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
    position: int | None = Field(default=0)
    article: Article
    created_at: datetime | None = None
    extra: dict[str, Any] | None = None
    headline: str | None = None
    subhead: str | None = None
    preview_image_id: UUID | None = None
    feedback: bool | None = None
    position_in_section: int | None = None

    def model_post_init(self, __context):
        """This function is automatically called by the pydantic framework after the model object is initialized."""
        self.headline = self.headline or self.article.headline
        self.subhead = self.subhead or self.article.subhead
        self.preview_image_id = self.preview_image_id or self.article.preview_image_id


class ImpressedSection(BaseModel):
    section_id: UUID | None = None
    title: str | None = None
    flavor: str | None = None
    personalized: bool = True
    seed_entity_id: UUID | None = None
    impressions: list[Impression] = Field(default_factory=list)
    position: int | None = None

    @classmethod
    def from_articles(
        cls,
        articles,
        extras=None,
        title: str | None = None,
        flavor: str | None = None,
        seed_entity_id: UUID | None = None,
        personalized: bool = True,
    ):
        extras = extras or []
        return ImpressedSection(
            impressions=[
                Impression(position=idx + 1, article=article, extra=extra)
                for idx, (article, extra) in enumerate(zip_longest(articles, extras))
            ],
            title=title,
            flavor=flavor,
            seed_entity_id=seed_entity_id,
            personalized=personalized,
        )


class Newsletter(BaseModel):
    newsletter_id: UUID = Field(default_factory=uuid4)
    account_id: UUID
    treatment_id: UUID | None = None
    experience_id: UUID | None = None
    sections: list[ImpressedSection]
    subject: str
    body_html: str
    created_at: datetime | None = None
    recommender_info: RecommenderInfo | None = None
    feedback: str | None = None

    @property
    def impressions(self) -> list[Impression]:
        imp = []
        for section in self.sections:
            imp.extend(section.impressions)
        return imp

    @property
    def articles(self) -> list[Article]:
        return [impression.article for impression in self.impressions]
