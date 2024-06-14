from uuid import UUID

from pydantic import BaseModel


class Account(BaseModel):
    account_id: UUID = None
    email: str
    source: str


class AccountInterest(BaseModel):
    account_id: UUID = None
    entity_id: UUID
    entity_name: str
    preference: int
    frequency: int
