from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel


from poprox_concepts.domain.click_history import ClickHistory
from poprox_concepts.domain.account import AccountInterest


class InterestProfile(BaseModel):
    click_history: ClickHistory
    click_topic_counts: Optional[Dict[str, int]] = None
    onboarding_topics: List[AccountInterest]
