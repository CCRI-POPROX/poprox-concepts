from poprox_concepts.api.recommendations.v1 import RecommendationRequestV1, RecommendationResponseV1
from poprox_concepts.api.recommendations.v2 import RecommendationRequestV2, RecommendationResponseV2
from poprox_concepts.api.recommendations.v3 import RecommendationRequestV3, RecommendationResponseV3
from poprox_concepts.api.recommendations.v4 import RecommendationRequestV4, RecommendationResponseV4

RecommendationRequest = RecommendationRequestV1
RecommendationResponse = RecommendationResponseV1

__all__ = [
    "RecommendationRequest",
    "RecommendationRequestV1",
    "RecommendationRequestV2",
    "RecommendationRequestV3",
    "RecommendationRequestV4",
    "RecommendationResponse",
    "RecommendationResponseV1",
    "RecommendationResponseV2",
    "RecommendationResponseV3",
    "RecommendationResponseV4",
]
