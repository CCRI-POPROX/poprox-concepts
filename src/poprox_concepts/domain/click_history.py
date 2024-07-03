from uuid import UUID

from pydantic import BaseModel


class ClickHistory(BaseModel):
    account_id: UUID | None = None
    article_ids: list[UUID]
