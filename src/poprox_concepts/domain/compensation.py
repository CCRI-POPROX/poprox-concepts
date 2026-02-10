from datetime import date, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CompensationPeriod(BaseModel):
    compensation_id: UUID | None = Field(default_factory=uuid4)
    name: str | None = None
    start_date: date
    end_date: date
    created_at: datetime | None = None

    @property
    def active(self) -> bool:
        now = date.today()
        return self.start_date <= now and self.end_date >= now
