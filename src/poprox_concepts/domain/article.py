from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Entity(BaseModel):
    entity_id: UUID | None = None
    external_id: str | None = None
    name: str
    entity_type: str
    source: str
    raw_data: dict[str, Any] | None


class Mention(BaseModel):
    article_id: UUID | None = None
    mention_id: UUID | None = None
    source: str
    relevance: float
    entity: Entity


class Article(BaseModel):
    article_id: UUID | None = None
    title: str
    content: str | None = None
    url: str | None = None
    published_at: datetime = datetime(1970, 1, 1, 0, 0, tzinfo=timezone.utc)
    mentions: list[Mention] = []
    source: str | None = None
    external_id: str | None = None
    raw_data: dict[str, Any] | None


class ArticleSet(BaseModel):
    model_config = ConfigDict(extra="allow")

    articles: list[Article]
