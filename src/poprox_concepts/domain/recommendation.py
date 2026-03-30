from datetime import datetime
from typing import TypeAlias
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from poprox_concepts.domain import Article
from poprox_concepts.domain.account import EntityType

Extra: TypeAlias = dict[str, JsonValue]


class CandidatePool(BaseModel):
    model_config = ConfigDict(extra="allow")

    pool_id: UUID | None = None
    pool_type: str | None = None

    seed_entity_id: UUID | None = None
    seed_entity_name: str | None = None
    seed_entity_type: EntityType | None = None

    created_at: datetime | None = None

    articles: list[Article]


CandidateSet: TypeAlias = CandidatePool


class RecommendationList(BaseModel):
    articles: list[Article] = Field(default_factory=list)
    extras: list[Extra] = Field(default_factory=list)
