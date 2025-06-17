from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class Experience(BaseModel):
    experience_id: UUID | None = None
    name: str
    recommender_id: UUID
    team_id: UUID
    start_date: date
    end_date: date
    created_at: datetime | None = None
    frequency: str | None = None
