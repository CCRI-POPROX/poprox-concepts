from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt

from poprox_concepts.domain import Article, InterestProfile


class RecommendationRequest(BaseModel):
    todays_articles: list[Article]
    past_articles: list[Article]
    interest_profile: InterestProfile
    num_recs: PositiveInt


class RecommendationResponse(BaseModel):
    recommendations: dict[UUID, list[Article]]
    recommender: RecommenderInfo | None = Field(default=None)


class RecommenderInfo(BaseModel):
    """
    Identity and versioning metadata for the system that generated the provided
    recommendations.
    """

    name: str | None = Field(default=None)
    version: str | None = Field(default=None)
    hash: str | None = Field(default=None)
