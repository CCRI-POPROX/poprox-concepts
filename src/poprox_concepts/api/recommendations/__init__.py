from poprox_concepts.api.recommendations.v1 import RecommendationRequestV1, RecommendationResponseV1
from poprox_concepts.api.recommendations.v2 import RecommendationRequestV2, RecommendationResponseV2
from poprox_concepts.api.recommendations.versions import RecommenderInfo

RecommendationRequest = RecommendationRequestV1
RecommendationResponse = RecommendationResponseV1

__all__ = [
    RecommenderInfo,
    RecommendationRequest,
    RecommendationRequestV1,
    RecommendationRequestV2,
    RecommendationResponse,
    RecommendationResponseV1,
    RecommendationResponseV2,
]
