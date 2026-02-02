from collections.abc import Iterable
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from poprox_concepts.domain.account import AccountInterest, EntityType
from poprox_concepts.domain.click import Click


class InterestProfile(BaseModel):
    # This allows extra properties to be added to the model that it isn't expecting,
    # which is useful for allowing the recommender to enrich the interest profile with
    # additional information (like user embeddings).
    #
    # However, allowing extra properties to be added by downstream code means we have to
    # be careful that anything that we expect to always be present DOES NOT have a default
    # value in the list of attributes below. Supplying a default makes that field optional,
    # which means that parsing and validation won't expect it to be present. This can result
    # in unexpected behavior when renaming attributes, since neither supplying an unexpected
    # attribute name nor failing to provide an expected attribute name will cause an error
    # if a default is supplied.
    model_config = ConfigDict(extra="allow")

    profile_id: UUID | None = None
    entity_interests: list[AccountInterest]
    click_history: list[Click]
    click_topic_counts: dict[str, int] | None = None
    click_locality_counts: dict[str, int] | None = None
    article_feedbacks: dict[UUID, bool] | None = None
    impressed_article_ids: list[UUID] = []

    def interests_by_type(self, entity_type: EntityType) -> Iterable[AccountInterest]:
        return (ai for ai in self.entity_interests if ai.entity_type == entity_type)

    @property
    def onboarding_topics(self) -> Iterable[AccountInterest]:
        """
        .. deprecated:: 1.0
            Use :meth:`interests_by_type` with "topic" instead.
        """
        return self.interests_by_type("topic")
