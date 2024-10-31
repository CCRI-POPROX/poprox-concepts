from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


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
    published_at: datetime = datetime(1970, 1, 1, 0, 0, tzinfo=timezone.utc)
    mentions: list[Mention] = []
    source: str | None = None
    external_id: str | None = None
    raw_data: dict[str, Any] | None = None


class ArticleSet(BaseModel):
    model_config = ConfigDict(extra="allow")

    articles: list[Article]


class ArticlePlacement(BaseModel):
    article_id: UUID = Field(default_factory=uuid4)
    url: str | None = None
    section: str | None = None
    level: str | None = None
    image_url: str | None = None
    created_at: datetime = datetime.now(timezone.utc)
