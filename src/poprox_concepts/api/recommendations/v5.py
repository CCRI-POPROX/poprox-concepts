from __future__ import annotations

from typing import TypeAlias
from uuid import UUID

from pydantic import BaseModel, Field, JsonValue, PositiveInt

from poprox_concepts.api.recommendations.versions import ProtocolVersions
from poprox_concepts.domain import ArticlePackage, CandidateSet, ImpressedSection, InterestProfile
from poprox_concepts.domain.newsletter import RecommenderInfo

Extra: TypeAlias = dict[str, JsonValue]


class ProtocolModelV5_0(BaseModel):
    """
    Version 5.0 of the POPROX protocol has embeddings in recommendation requests.
    """

    protocol_version: ProtocolVersions = Field(default=ProtocolVersions.VERSION_5_0, frozen=True)


class RecommendationRequestV5(ProtocolModelV5_0):
    candidates: CandidateSet
    interacted: CandidateSet
    interest_profile: InterestProfile
    num_recs: PositiveInt
    embeddings: dict[UUID, dict[str, list[float]]] | None = Field(default=None)
    article_packages: list[ArticlePackage] = Field(default_factory=list)


class RecommendationResponseV5(ProtocolModelV5_0):
    recommendations: list[ImpressedSection]
    recommender: RecommenderInfo | None = Field(default=None)
