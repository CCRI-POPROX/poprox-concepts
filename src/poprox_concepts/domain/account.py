from uuid import UUID

from pydantic import BaseModel


class Account(BaseModel):
    account_id: UUID = None
    email: str
    zip5: str
    status: str
    source: str | None = None


class AccountInterest(BaseModel):
    account_id: UUID = None
    entity_id: UUID
    entity_name: str
    preference: int | None
    frequency: int | None
