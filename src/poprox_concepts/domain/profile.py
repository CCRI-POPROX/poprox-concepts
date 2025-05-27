from uuid import UUID

from pydantic import BaseModel, ConfigDict

from poprox_concepts.domain.account import AccountInterest
from poprox_concepts.domain.click import Click
from poprox_concepts.domain.article import Article


class InterestProfile(BaseModel):
    model_config = ConfigDict(extra="allow")

    profile_id: UUID | None = None
    click_history: list[Click]
    click_topic_counts: dict[str, int] | None = None
    click_locality_counts: dict[str, int] | None = None
    article_feedbacks: dict[UUID, bool] | None = None 
    onboarding_topics: list[AccountInterest]
  