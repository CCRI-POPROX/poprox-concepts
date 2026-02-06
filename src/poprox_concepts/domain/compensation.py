from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

class Compensation(BaseModel):
   compensation_id: UUID | None = Field(default_factory=uuid4)
   name: str | None = None
   start_date: datetime | None = None
   end_date: datetime | None = None
   created_at: datetime | None = None
