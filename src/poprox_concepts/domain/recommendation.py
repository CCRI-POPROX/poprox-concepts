from itertools import zip_longest
from typing import TypeAlias

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from poprox_concepts.domain import Article, Impression

Extra: TypeAlias = dict[str, JsonValue]


class CandidateSet(BaseModel):
    model_config = ConfigDict(extra="allow")

    articles: list[Article]


class RecommendationList(BaseModel):
    articles: list[Article] = Field(default_factory=list)
    extras: list[Extra] = Field(default_factory=list)


class ImpressedRecommendations(BaseModel):
    impressions: list[Impression] = Field(default_factory=list)

    @classmethod
    def from_articles(cls, articles, extras=None):
        extras = extras or []
        return ImpressedRecommendations(
            impressions=[
                Impression(position=idx + 1, article=article, extra=extra)
                for idx, (article, extra) in enumerate(zip_longest(articles, extras))
            ]
        )
