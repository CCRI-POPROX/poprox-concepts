from pydantic import BaseModel, ConfigDict

from poprox_concepts.domain.article import Article


class CandidateSet(BaseModel):
    model_config = ConfigDict(extra="allow")

    articles: list[Article]

class RecommendationList(BaseModel):
    model_config = ConfigDict(extra="allow")

    articles: list[Article]
