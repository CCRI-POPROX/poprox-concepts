from uuid import UUID

from pydantic import BaseModel, ConfigDict

from poprox_concepts.domain.account import AccountInterest
from poprox_concepts.domain.click_history import ClickHistory


class InterestProfile(BaseModel):
    model_config = ConfigDict(extra="allow")

    profile_id: UUID | None = None
    click_history: ClickHistory
    click_topic_counts: dict[str, int] | None = None
    onboarding_topics: list[AccountInterest]
