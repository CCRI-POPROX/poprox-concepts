from typing import TypeAlias

from pydantic import BaseModel, ConfigDict, Field

from poprox_concepts.domain.article import Article

PrimitiveTypes: TypeAlias = bool | int | float | str | bytes | None
ValueTypes: TypeAlias = BaseModel | PrimitiveTypes

CollectionTypes: TypeAlias = list[ValueTypes] | set[ValueTypes] | dict[ValueTypes, ValueTypes] | tuple[ValueTypes, ...]

RecursiveCollectionTypes: TypeAlias = (
    list[CollectionTypes] | set[CollectionTypes] | dict[ValueTypes, CollectionTypes] | tuple[CollectionTypes, ...]
)

SerializableTypes: TypeAlias = ValueTypes | CollectionTypes | RecursiveCollectionTypes
Extra: TypeAlias = dict[str, SerializableTypes]


class CandidateSet(BaseModel):
    model_config = ConfigDict(extra="allow")

    articles: list[Article]


class RecommendationList(BaseModel):
    articles: list[Article] = Field(default_factory=list)
    extras: list[Extra] = Field(default_factory=list)
