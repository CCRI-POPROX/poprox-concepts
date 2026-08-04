from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, PositiveInt, field_validator, model_validator

from poprox_concepts.api.recommendations.versions import ProtocolVersions
from poprox_concepts.domain import Article, ArticlePackage, CandidateSet, InterestProfile
from poprox_concepts.domain.newsletter import ImpressedSection, Impression, RecommenderInfo


class ProtocolModelV6_0(BaseModel):
    """Version 6.0 separates article metadata from default recommendation eligibility."""

    protocol_version: ProtocolVersions = Field(
        default=ProtocolVersions.VERSION_6_0,
        frozen=True,
    )

    @field_validator("protocol_version")
    @classmethod
    def _require_v6_protocol(cls, version: ProtocolVersions) -> ProtocolVersions:
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
    def _validate_article_references(self) -> RecommendationRequestV6:
        # Catalog article IDs must be unique.
        article_ids = [article.article_id for article in self.articles]
        duplicate_count = len(article_ids) - len(set(article_ids))
        if duplicate_count:
            raise ValueError(f"articles duplicate article ID count: {duplicate_count}")

        # Package IDs must be unique, and the default package must be present.
        package_ids = [package.package_id for package in self.article_packages]
        duplicate_count = len(package_ids) - len(set(package_ids))
        if duplicate_count:
            raise ValueError(f"article_packages duplicate package ID count: {duplicate_count}")

        if self.default_package_id not in package_ids:
            raise ValueError(f"default_package_id {self.default_package_id} does not match an article package")

        # Package references must be unique within each package and resolve to the catalog.
        catalog_ids = set(article_ids)
        for package in self.article_packages:
            duplicate_count = len(package.article_ids) - len(set(package.article_ids))
            if duplicate_count:
                raise ValueError(f"article package {package.package_id} duplicate article ID count: {duplicate_count}")

            unknown_references = sorted(set(package.article_ids) - catalog_ids, key=str)
            if unknown_references:
                raise ValueError(
                    f"article package {package.package_id} unknown article reference count: {len(unknown_references)}; "
                    f"first unknown ID: {unknown_references[0]}"
                )

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
