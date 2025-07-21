from datetime import date, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Experience(BaseModel):
    experience_id: UUID | None = Field(default_factory=uuid4)
    recommender_id: UUID
    team_id: UUID | None
    name: str
    start_date: date
    end_date: date | None = None
    created_at: datetime | None = None
    template: str | None = None

    @property
    def active(self) -> bool:
        now = date.today()
        return self.start_date <= now and (self.end_date is None or self.end_date >= now)
