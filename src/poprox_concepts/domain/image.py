from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class Image(BaseModel):
    image_id: UUID | None = None
    article_id: UUID | None = None
    url: str
    source: str
    external_id: str | None = None
    raw_data: dict[str, Any] | None
