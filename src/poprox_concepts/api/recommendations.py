from __future__ import annotations

from pydantic import BaseModel, Field, PositiveInt

from poprox_concepts.domain import CandidateSet, InterestProfile, RecommendationList


class RecommendationRequest(BaseModel):
    candidates: CandidateSet
    interacted: CandidateSet
    interest_profile: InterestProfile
    num_recs: PositiveInt


class RecommendationResponse(BaseModel):
    recommendations: RecommendationList
    recommender: RecommenderInfo | None = Field(default=None)


class RecommenderInfo(BaseModel):
    """
    Identity and versioning metadata for the system that generated the provided
    recommendations.
    """

    name: str | None = None
    version: str | None = None
    hash: str | None = None
