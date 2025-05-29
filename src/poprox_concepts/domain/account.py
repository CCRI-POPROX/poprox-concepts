from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Account(BaseModel):
    account_id: UUID = None
    email: str | None = None
    zip5: str | None = None
    compensation: str | None = None
    status: str
    source: str | None = None
    subsource: str | None = None
    placebo_id: str | None = None
    created_at: datetime | None = None


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

INTERNAL_ACCOUNT_SOURCES = [
    "friends_of_poprox",
    "team",
    "test",
    "kluver",
]

EXTERNAL_ACCOUNT_SOURCES = [
    "website",
    "ff",
    "ml-volunteers",
]


# NOTE: these are not opposites -- a user may be _neither_ internal nor external if the source code is not recognized.
def is_internal_account(account: Account) -> bool:
    return account.source is not None and account.source in INTERNAL_ACCOUNT_SOURCES


def is_external_account(account: Account) -> bool:
    return account.source is not None and account.source in EXTERNAL_ACCOUNT_SOURCES
