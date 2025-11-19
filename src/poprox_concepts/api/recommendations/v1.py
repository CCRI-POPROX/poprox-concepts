from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from poprox_concepts.api.recommendations.versions import ProtocolVersions
from poprox_concepts.domain.article import Article
from poprox_concepts.domain.click import Click
from poprox_concepts.domain.newsletter import RecommenderInfo


class ProtocolModelV1_1(BaseModel):
    """
    Version 1.1 of the POPROX protocol added the `recommender` field to `RecommendationResponse`
    to allow the platform to track which specific recommendation pipeline generated the returned
    recommendations
    """

    protocol_version: ProtocolVersions = Field(default=ProtocolVersions.VERSION_1_1, frozen=True)


class AccountInterestV1(BaseModel):
    account_id: UUID | None = None
    entity_id: UUID
    entity_name: str
    preference: int
    frequency: int | None = None


class InterestProfileV1(BaseModel):
    model_config = ConfigDict(extra="allow")

    profile_id: UUID | None = None
    click_history: list[Click]
    click_topic_counts: dict[str, int] | None = None
    click_locality_counts: dict[str, int] | None = None
    onboarding_topics: list[AccountInterestV1]


class RecommendationRequestV1(ProtocolModelV1_1):
    todays_articles: list[Article]
    past_articles: list[Article]
    interest_profile: InterestProfileV1
    num_recs: PositiveInt


class RecommendationResponseV1(ProtocolModelV1_1):
    recommendations: dict[UUID, list[Article]]
    recommender: RecommenderInfo | None = Field(default=None)
