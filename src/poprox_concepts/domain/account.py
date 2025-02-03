from uuid import UUID

from pydantic import BaseModel


class Account(BaseModel):
    account_id: UUID = None
    email: str
    zip5: str | None = None
    compensation: str | None = None
    status: str
    source: str | None = None
    subsource: str | None = None
    placebo_id: str | None = None


class AccountInterest(BaseModel):
    account_id: UUID | None = None
    entity_id: UUID
    entity_name: str
    preference: int
    frequency: int | None = None


COMPENSATION_CHARITY_OPTIONS = [
    "American Red Cross",
    "American Cancer Society",
    "Boys & Girls Club of America",
]


COMPENSATION_CARD_OPTIONS = [
    "Amazon",
    "Target",
    "Walmart",
    "Tango",
]
