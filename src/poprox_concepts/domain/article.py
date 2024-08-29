from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field
from enum import Enum

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

class Popularity(str, Enum):
    story_1 = 'Story 1'
    story_2 = 'Story 2'
    story_3 = 'Story 3'
    missing = 'Missing'

class Article(BaseModel):
    article_id: UUID = Field(default_factory=uuid4)
    title: str
    content: str | None = None
    url: str | None = None
    preview_image_id: UUID | None = None
    published_at: datetime = datetime(1970, 1, 1, 0, 0, tzinfo=timezone.utc)
    mentions: list[Mention] = []
    source: str | None = None
    external_id: str | None = None
    raw_data: dict[str, Any] | None = None
    popularity: Popularity = Popularity.missing

class ArticleSet(BaseModel):
    model_config = ConfigDict(extra="allow")

    articles: list[Article]
