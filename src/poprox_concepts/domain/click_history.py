from uuid import UUID

from pydantic import BaseModel


class ClickHistory(BaseModel):
    article_ids: list[UUID]
