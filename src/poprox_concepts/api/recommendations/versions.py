from enum import Enum

from pydantic import BaseModel

from poprox_concepts.domain.newsletter import RecommenderInfo


class ProtocolVersions(Enum):
    VERSION_1_1 = "1.1-2024-08-08"
    VERSION_2_0 = "2.0-2025-02-12"
    VERSION_3_0 = "3.0-2025-07-25"
    VERSION_4_0 = "4.0-2025-10-20"
