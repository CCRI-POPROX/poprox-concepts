from enum import Enum

from pydantic import BaseModel


class ProtocolVersions(Enum):
    VERSION_1_1 = "1.1-2024-08-08"
    VERSION_2_0 = "2.0-2025-02-12"


class RecommenderInfo(BaseModel):
    """
    Identity and versioning metadata for the system that generated the provided
    recommendations.
    """

    name: str | None = None
    version: str | None = None
    hash: str | None = None
