from poprox_concepts.api.recommendations.v5 import RecommendationRequestV5
from poprox_concepts.domain.profile import InterestProfile
from poprox_concepts.domain.recommendation import CandidateSet


def test_create_request_without_impressed_list():
    """A simple test that attempts to create a recommendationRequestV5 without passing in the impressed list."""
    empty_set = CandidateSet(articles=[])
    interest_profile = InterestProfile(entity_interests=[], click_history=[])
    RecommendationRequestV5(
        candidates=empty_set,
        interacted=empty_set,
        interest_profile=interest_profile,
        num_recs=10,
        embeddings={},
        article_packages=[],
    )


def test_parse_request_without_impressed_list():
    raw = """{
  "candidates": {
    "articles": []
  },
  "interacted": {
    "articles": []
  },
  "interest_profile": {
    "entity_interests": [],
    "click_history": []
  },
  "num_recs": 10,
  "embeddings": {},
  "article_packages": []
}"""
    RecommendationRequestV5.model_validate_json(raw)
