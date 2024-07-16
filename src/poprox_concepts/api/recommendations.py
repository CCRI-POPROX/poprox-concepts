from uuid import UUID

from pydantic import BaseModel, PositiveInt

from poprox_concepts.domain import Article, InterestProfile


class RecommendationRequest(BaseModel):
    todays_articles: list[Article]
    past_articles: list[Article]
    interest_profile: InterestProfile
    num_recs: PositiveInt


class RecommendationResponse(BaseModel):
    recommendations: dict[UUID, list[Article]]
