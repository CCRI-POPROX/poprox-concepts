from datetime import datetime
from typing import TypeAlias
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from poprox_concepts.domain import Article

Extra: TypeAlias = dict[str, JsonValue]


class CandidatePool(BaseModel):
    model_config = ConfigDict(extra="allow")

    pool_id: UUID | None = Field(default_factory=uuid4)
    pool_type: str | None = None
    created_at: datetime | None = None

    articles: list[Article]


CandidateSet: TypeAlias = CandidatePool


class RecommendationList(BaseModel):
    articles: list[Article] = Field(default_factory=list)
    extras: list[Extra] = Field(default_factory=list)
