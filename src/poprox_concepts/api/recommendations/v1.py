from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt

from poprox_concepts.api.recommendations.versions import ProtocolVersions, RecommenderInfo
from poprox_concepts.domain.article import Article
from poprox_concepts.domain.profile import InterestProfile


class ProtocolModelV1_1(BaseModel):
    """
    Version 1.1 of the POPROX protocol added the `recommender` field to `RecommendationResponse`
    to allow the platform to track which specific recommendation pipeline generated the returned
    recommendations
    """

    protocol_version: ProtocolVersions = Field(default=ProtocolVersions.VERSION_1_1, frozen=True)


class RecommendationRequestV1(ProtocolModelV1_1):
    todays_articles: list[Article]
    past_articles: list[Article]
    interest_profile: InterestProfile
    num_recs: PositiveInt


class RecommendationResponseV1(ProtocolModelV1_1):
    recommendations: dict[UUID, list[Article]]
    recommender: RecommenderInfo | None = Field(default=None)
