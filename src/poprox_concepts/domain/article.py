from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from poprox_concepts.domain.image import Image


class Entity(BaseModel):
    entity_id: UUID | None = None
    external_id: str | None = None
    name: str
    entity_type: str
    source: str
    raw_data: dict[str, Any] | None = None


class Mention(BaseModel):
    article_id: UUID | None = None
    mention_id: UUID | None = None
    source: str
    relevance: float
    entity: Entity


class Article(BaseModel):
    article_id: UUID = Field(default_factory=uuid4)
    headline: str
    subhead: str | None = None
    body: str | None = None
    url: str | None = None
    preview_image_id: UUID | None = None
    mentions: list[Mention] = []
    linked_articles: dict[UUID, str] = {}
    source: str | None = None
    external_id: str | None = None
    raw_data: dict[str, Any] | None = None
    images: list[Image] | None = None
    published_at: datetime = datetime(1970, 1, 1, 0, 0, tzinfo=timezone.utc)
    created_at: datetime | None = None


# What we get from AP and use at ingestion time
class TopStoryPackage(BaseModel):
    package_id: UUID | None = None
    entity: Entity
    articles: list[UUID]
    as_of: datetime
    created_at: datetime = datetime.now(timezone.utc)


# What we send to the recommender
# We want this to be able to account for "most clicked yesterday"
class TopStories(BaseModel):
    source: str
    entity: Entity | None = None
    article_ids: list[UUID]


class ArticlePlacement(BaseModel):
    placement_id: UUID = Field(default_factory=uuid4)
    article_id: UUID
    url: str | None = None
    section: str | None = None
    level: str | None = None
    image_url: str | None = None
    created_at: datetime = datetime.now(timezone.utc)
