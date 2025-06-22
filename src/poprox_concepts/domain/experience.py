from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class Experience(BaseModel):
    experience_id: UUID | None = None
    recommender_id: UUID
    team_id: UUID
    name: str
    start_date: date
    end_date: date
    created_at: datetime | None = None
