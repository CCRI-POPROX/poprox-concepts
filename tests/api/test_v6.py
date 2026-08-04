from uuid import UUID

import pytest
from pydantic import ValidationError

from poprox_concepts.api.recommendations import (
    RecommendationRequest,
    RecommendationRequestV1,
    RecommendationRequestV6,
    RecommendationResponse,
    RecommendationResponseV1,
    RecommendationResponseV6,
)
from poprox_concepts.api.recommendations.v5 import RecommendationRequestV5
from poprox_concepts.api.recommendations.versions import ProtocolVersions
from poprox_concepts.domain import Article, ArticlePackage, CandidateSet, InterestProfile
from poprox_concepts.domain.newsletter import ImpressedSection, Impression

ARTICLE_1_ID = UUID(int=1)
ARTICLE_2_ID = UUID(int=2)
ARTICLE_3_ID = UUID(int=3)
UNKNOWN_ARTICLE_ID = UUID(int=99)
DEFAULT_PACKAGE_ID = UUID(int=101)
SECONDARY_PACKAGE_ID = UUID(int=102)
MISSING_PACKAGE_ID = UUID(int=199)


def article(article_id: UUID) -> Article:
    return Article(article_id=article_id, headline=f"Article {article_id.int}")


def package(package_id: UUID, article_ids: list[UUID]) -> ArticlePackage:
    return ArticlePackage(
        package_id=package_id,
        title=f"Package {package_id.int}",
        source="test",
        article_ids=article_ids,
    )


def request(
    articles: list[Article],
    article_packages: list[ArticlePackage],
    default_package_id: UUID,
) -> RecommendationRequestV6:
    return RecommendationRequestV6(
        articles=articles,
        interacted=CandidateSet(articles=[]),
        interest_profile=InterestProfile(entity_interests=[], click_history=[]),
        num_recs=15,
        embeddings={},
        article_packages=article_packages,
        default_package_id=default_package_id,
    )


def test_v6_request_round_trip_separates_catalog_from_default_package() -> None:
    articles = [article(ARTICLE_1_ID), article(ARTICLE_2_ID), article(ARTICLE_3_ID)]
    default_package = package(DEFAULT_PACKAGE_ID, [ARTICLE_1_ID, ARTICLE_2_ID])
    secondary_package = package(SECONDARY_PACKAGE_ID, [ARTICLE_2_ID, ARTICLE_3_ID])

    original = request(articles, [default_package, secondary_package], DEFAULT_PACKAGE_ID)
    restored = RecommendationRequestV6.model_validate_json(original.model_dump_json())

    assert restored == original
    assert ARTICLE_2_ID in default_package.article_ids and ARTICLE_2_ID in secondary_package.article_ids
    assert ARTICLE_3_ID not in default_package.article_ids

    empty = request(
        [],
        [package(DEFAULT_PACKAGE_ID, []), package(SECONDARY_PACKAGE_ID, [])],
        DEFAULT_PACKAGE_ID,
    )
    assert RecommendationRequestV6.model_validate_json(empty.model_dump_json()) == empty


@pytest.mark.parametrize(
    ("articles", "article_packages", "default_package_id", "message"),
    [
        (
            [article(ARTICLE_1_ID), article(ARTICLE_1_ID)],
            [package(DEFAULT_PACKAGE_ID, [ARTICLE_1_ID])],
            DEFAULT_PACKAGE_ID,
            "articles duplicate article ID count: 1",
        ),
        (
            [article(ARTICLE_1_ID)],
            [
                package(DEFAULT_PACKAGE_ID, [ARTICLE_1_ID]),
                package(DEFAULT_PACKAGE_ID, [ARTICLE_1_ID]),
            ],
            DEFAULT_PACKAGE_ID,
            "article_packages duplicate package ID count: 1",
        ),
        (
            [article(ARTICLE_1_ID)],
            [package(DEFAULT_PACKAGE_ID, [ARTICLE_1_ID, ARTICLE_1_ID])],
            DEFAULT_PACKAGE_ID,
            f"article package {DEFAULT_PACKAGE_ID} duplicate article ID count: 1",
        ),
        (
            [article(ARTICLE_1_ID)],
            [package(DEFAULT_PACKAGE_ID, [UNKNOWN_ARTICLE_ID])],
            DEFAULT_PACKAGE_ID,
            f"article package {DEFAULT_PACKAGE_ID} unknown article reference count: 1",
        ),
        (
            [article(ARTICLE_1_ID)],
            [package(DEFAULT_PACKAGE_ID, [ARTICLE_1_ID])],
            MISSING_PACKAGE_ID,
            f"default_package_id {MISSING_PACKAGE_ID} does not match an article package",
        ),
    ],
)
def test_v6_request_rejects_invalid_catalog_and_package_relationships(
    articles: list[Article],
    article_packages: list[ArticlePackage],
    default_package_id: UUID,
    message: str,
) -> None:
    with pytest.raises(ValidationError, match=message):
        request(articles, article_packages, default_package_id)


def test_v6_request_rejects_another_known_protocol_version() -> None:
    valid = request([], [package(DEFAULT_PACKAGE_ID, [])], DEFAULT_PACKAGE_ID)
    payload = valid.model_dump(mode="json")
    payload["protocol_version"] = ProtocolVersions.VERSION_5_0.value

    with pytest.raises(ValidationError, match="protocol_version must be 6.0-2026-07-23"):
        RecommendationRequestV6.model_validate(payload)


def test_v6_response_round_trip_preserves_flattened_impressions() -> None:
    impression = Impression(article=article(ARTICLE_1_ID))
    original = RecommendationResponseV6(recommendations=[ImpressedSection(title="Top News", impressions=[impression])])
    restored = RecommendationResponseV6.model_validate_json(original.model_dump_json())

    assert restored == original
    assert restored.impressions == [impression]


def test_v6_exports_do_not_change_existing_aliases_or_v5_shape() -> None:
    assert (RecommendationRequest, RecommendationResponse) == (RecommendationRequestV1, RecommendationResponseV1)
    v5 = RecommendationRequestV5(
        candidates=CandidateSet(articles=[]),
        interacted=CandidateSet(articles=[]),
        interest_profile=InterestProfile(entity_interests=[], click_history=[]),
        num_recs=1,
    )

    payload = v5.model_dump(mode="json")
    assert "candidates" in payload
    assert {"articles", "default_package_id"}.isdisjoint(payload)
