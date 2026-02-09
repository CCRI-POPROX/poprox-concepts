from datetime import date, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Compensation(BaseModel):
    compensation_id: UUID | None = Field(default_factory=uuid4)
    name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    created_at: datetime | None = None

    @property
    def active(self) -> bool:
        now = date.today()
        return self.start_date <= now and (self.end_date is None or self.end_date >= now)
