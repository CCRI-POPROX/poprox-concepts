from __future__ import annotations

from typing import TypeAlias

from pydantic import BaseModel, Field, JsonValue, PositiveInt

from poprox_concepts.api.recommendations.versions import ProtocolVersions, RecommenderInfo
from poprox_concepts.domain.newsletter import Impression
from poprox_concepts.domain.profile import InterestProfile
from poprox_concepts.domain.recommendation import CandidateSet


class ProtocolModelV3_0(BaseModel):
    """
    Version 3.0 of the POPROX protocol changed the return model of a recommendation to return a list of "sections"
    """

    protocol_version: ProtocolVersions = Field(default=ProtocolVersions.VERSION_3_0, frozen=True)


class RecommendationRequestV3(ProtocolModelV3_0):
    candidates: CandidateSet
    interacted: CandidateSet
    interest_profile: InterestProfile
    num_recs: PositiveInt


class RecommendationResponseSection(BaseModel):
    title: str
    recommendations: RecommendationList_v3


Extra: TypeAlias = dict[str, JsonValue]


class RecommendationList_v3(ProtocolModelV3_0):
    impressions: list[Impression] = Field(default_factory=list)
    extras: list[Extra] = Field(default_factory=list)


class RecommendationResponseV3(ProtocolModelV3_0):
    recommendations: list[RecommendationResponseSection]
    recommender: RecommenderInfo | None = Field(default=None)
