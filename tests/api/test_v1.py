from poprox_concepts.api.recommendations.v1 import RecommendationRequestV1, RecommendationResponseV1


def test_request_parsing():
    with open("tests/api/v1_request.json") as f:
        content = f.read()

    request = RecommendationRequestV1.model_validate_json(content)
    assert isinstance(request, RecommendationRequestV1)


def test_response_parsing():
    with open("tests/api/v1_response.json") as f:
        content = f.read()

    request = RecommendationResponseV1.model_validate_json(content)
    assert isinstance(request, RecommendationResponseV1)
