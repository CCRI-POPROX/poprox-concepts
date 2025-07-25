from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field, PositiveInt

from poprox_concepts.api.recommendations.versions import ProtocolVersions, RecommenderInfo
from poprox_concepts.domain.profile import InterestProfile
from poprox_concepts.domain.recommendation import CandidateSet, RecommendationList


class ProtocolModelV3_0(BaseModel):
    """
    Version 3.0 of the POPROX protocol has embeddings in recommendation requests.
    """

    protocol_version: ProtocolVersions = Field(default=ProtocolVersions.VERSION_3_0, frozen=True)


class RecommendationRequestV3(ProtocolModelV3_0):
    candidates: CandidateSet
    interacted: CandidateSet
    interest_profile: InterestProfile
    num_recs: PositiveInt
    embeddings: dict[UUID, list[float]]


class RecommendationResponseV3(ProtocolModelV3_0):
    recommendations: RecommendationList
    recommender: RecommenderInfo | None = Field(default=None)
