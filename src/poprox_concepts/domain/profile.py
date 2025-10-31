from collections.abc import Iterable
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from poprox_concepts.domain.account import AccountInterest, EntityType
from poprox_concepts.domain.click import Click


class InterestProfile(BaseModel):
    model_config = ConfigDict(extra="allow")

    profile_id: UUID | None = None
    click_history: list[Click]
    click_topic_counts: dict[str, int] | None = None
    click_locality_counts: dict[str, int] | None = None
    article_feedbacks: dict[UUID, bool] | None = None
    entity_interests: list[AccountInterest] = []

    def interests_by_type(
        self, entity_type: EntityType
    ) -> Iterable[AccountInterest]:
        return (ai for ai in self.entity_interests if ai.entity_type == entity_type)

    @property
    def onboarding_topics(self) -> Iterable[AccountInterest]:
        """
        .. deprecated:: 1.0
            Use :meth:`interests_by_type` with "topic" instead.
        """
        return self.interests_by_type("topic")
