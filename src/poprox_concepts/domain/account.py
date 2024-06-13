from uuid import UUID

from pydantic import BaseModel


class Account(BaseModel):
    account_id: UUID = None
    email: str


class Account_Interest(BaseException):
    account_id: UUID = None
    entity_id: UUID
    preference: int
    frequency: int
