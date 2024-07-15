from uuid import UUID

from pydantic import BaseModel


class Click(BaseModel):
    article_id: UUID