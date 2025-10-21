from __future__ import annotations

from pydantic import BaseModel, Field, PositiveInt

from poprox_concepts.api.recommendations.versions import ProtocolVersions
from poprox_concepts.domain.newsletter import RecommenderInfo
from poprox_concepts.domain.profile import InterestProfile
from poprox_concepts.domain.recommendation import CandidateSet, RecommendationList


class ProtocolModelV2_0(BaseModel):
    """
    Version 2.0 of the POPROX protocol changed the names of types of the fields representing
    interacted and candidate items, as well as the returned recommendations
    """

    protocol_version: ProtocolVersions = Field(default=ProtocolVersions.VERSION_2_0, frozen=True)


class RecommendationRequestV2(ProtocolModelV2_0):
    candidates: CandidateSet
    interacted: CandidateSet
    interest_profile: InterestProfile
    num_recs: PositiveInt


class RecommendationResponseV2(ProtocolModelV2_0):
    recommendations: RecommendationList
    recommender: RecommenderInfo | None = Field(default=None)
