from typing import Any
from uuid import UUID

from pydantic import BaseModel


class Image(BaseModel):
    image_id: UUID | None = None
    url: str
    caption: str | None = None
    source: str
    external_id: str | None = None
    raw_data: dict[str, Any] | None
