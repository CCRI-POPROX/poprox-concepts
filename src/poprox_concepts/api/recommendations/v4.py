from __future__ import annotations

from typing import TypeAlias
from uuid import UUID

from pydantic import BaseModel, Field, JsonValue, PositiveInt

from poprox_concepts.api.recommendations.versions import ProtocolVersions
from poprox_concepts.domain import CandidateSet, InterestProfile
from poprox_concepts.domain.newsletter import ImpressedSection, RecommenderInfo

Extra: TypeAlias = dict[str, JsonValue]


class ProtocolModelV4_0(BaseModel):
    """
    Version 4.0 of the POPROX protocol has embeddings in recommendation requests.
    """

    protocol_version: ProtocolVersions = Field(default=ProtocolVersions.VERSION_4_0, frozen=True)


class RecommendationRequestV4(ProtocolModelV4_0):
    candidates: CandidateSet
    interacted: CandidateSet
    interest_profile: InterestProfile
    num_recs: PositiveInt
    embeddings: dict[UUID, dict[str, list[float]]] | None = Field(default=None)


class RecommendationResponseV4(ProtocolModelV4_0):
    recommendations: ImpressedSection
    recommender: RecommenderInfo | None = Field(default=None)
