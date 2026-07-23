from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, PositiveInt, field_validator, model_validator

from poprox_concepts.api.recommendations.versions import ProtocolVersions
from poprox_concepts.domain import Article, ArticlePackage, CandidateSet, InterestProfile
from poprox_concepts.domain.newsletter import ImpressedSection, Impression, RecommenderInfo


def _duplicate_ids(values: Iterable[UUID]) -> list[UUID]:
    counts = Counter(values)
    return sorted((value for value, count in counts.items() if count > 1), key=str)


class ProtocolModelV6_0(BaseModel):
    """Version 6.0 separates article metadata from default recommendation eligibility."""

    protocol_version: ProtocolVersions = Field(
        default=ProtocolVersions.VERSION_6_0,
        frozen=True,
    )

    @field_validator("protocol_version")
    @classmethod
    def require_v6_protocol(cls, version: ProtocolVersions) -> ProtocolVersions:
        if version != ProtocolVersions.VERSION_6_0:
            raise ValueError(f"protocol_version must be {ProtocolVersions.VERSION_6_0.value}")
        return version


class RecommendationRequestV6(ProtocolModelV6_0):
    request_id: UUID = Field(default_factory=uuid4)
    requested_at: datetime = Field(default_factory=lambda: datetime.now())

    articles: list[Article]
    interacted: CandidateSet
    interest_profile: InterestProfile
    num_recs: PositiveInt
    embeddings: dict[UUID, dict[str, list[float]]] | None = Field(default=None)
    article_packages: list[ArticlePackage]
    default_package_id: UUID
    impressed_article_ids: list[UUID] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_article_references(self) -> RecommendationRequestV6:
        article_ids = [article.article_id for article in self.articles]
        duplicate_article_ids = _duplicate_ids(article_ids)
        if duplicate_article_ids:
            duplicates = ", ".join(str(article_id) for article_id in duplicate_article_ids)
            raise ValueError(f"articles contains duplicate article IDs: {duplicates}")

        package_ids = [package.package_id for package in self.article_packages]
        duplicate_package_ids = _duplicate_ids(package_ids)
        if duplicate_package_ids:
            duplicates = ", ".join(str(package_id) for package_id in duplicate_package_ids)
            raise ValueError(f"article_packages contains duplicate package IDs: {duplicates}")

        if self.default_package_id not in package_ids:
            raise ValueError(f"default_package_id {self.default_package_id} does not match an article package")

        catalog_ids = set(article_ids)
        for package in self.article_packages:
            duplicate_references = _duplicate_ids(package.article_ids)
            if duplicate_references:
                duplicates = ", ".join(str(article_id) for article_id in duplicate_references)
                raise ValueError(f"article package {package.package_id} contains duplicate article IDs: {duplicates}")

            unknown_references = sorted(set(package.article_ids) - catalog_ids, key=str)
            if unknown_references:
                unknown = ", ".join(str(article_id) for article_id in unknown_references)
                raise ValueError(f"article package {package.package_id} references unknown article IDs: {unknown}")

        return self


class RecommendationResponseV6(ProtocolModelV6_0):
    request_id: UUID | None = None

    recommendations: list[ImpressedSection]
    recommender: RecommenderInfo | None = Field(default=None)

    @property
    def impressions(self) -> list[Impression]:
        impressions = []
        for section in self.recommendations:
            impressions.extend(section.impressions)
        return impressions
