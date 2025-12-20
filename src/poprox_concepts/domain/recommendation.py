from typing import TypeAlias

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from poprox_concepts.domain import Article

Extra: TypeAlias = dict[str, JsonValue]


class CandidateSet(BaseModel):
    model_config = ConfigDict(extra="allow")

    articles: list[Article]


class RecommendationList(BaseModel):
    articles: list[Article] = Field(default_factory=list)
    extras: list[Extra] = Field(default_factory=list)
