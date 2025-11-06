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
    relevance: float | None = None
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


class ArticlePackage(BaseModel):
    package_id: UUID | None = None
    title: str
    source: str
    seed: Entity | None = None
    article_ids: list[UUID]
    current_as_of: datetime | None = None
    created_at: datetime | None = None


class ArticlePlacement(BaseModel):
    placement_id: UUID = Field(default_factory=uuid4)
    article_id: UUID
    url: str | None = None
    section: str | None = None
    level: str | None = None
    image_url: str | None = None
    created_at: datetime = datetime.now(timezone.utc)


# Deprecated, will be removed
class TopNewsHeadline(BaseModel):
    article_id: UUID | None = None
    entity_id: UUID | None = None
    topic: str
    headline: str
    position: int
    as_of: datetime
