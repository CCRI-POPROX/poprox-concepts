from typing import Dict, List
from uuid import UUID

from pydantic import BaseModel, PositiveInt

from poprox_concepts.domain import Article, ClickHistory


class RecommendationRequest(BaseModel):
    todays_articles: List[Article]
    past_articles: List[Article]
    click_histories: List[ClickHistory]
    num_recs: PositiveInt


class RecommendationResponse(BaseModel):
    recommendations: Dict[UUID, List[Article]]
