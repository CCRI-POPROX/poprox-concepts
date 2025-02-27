from uuid import UUID

from pydantic import BaseModel


class Demographics(BaseModel):
    demographic_id: UUID = None
    account_id: UUID
    gender: str
    birth_year: int
    zip3: str
    education: str
    race: str
    email_client: str | None = None


GENDER_OPTIONS = ["Woman", "Man", "Non-binary", "Other", "Prefer not to say"]


EDUCATION_OPTIONS = [
    "Some high school",
    "High school",
    "Some college",
    "Trade, technical or vocational training",
    "Associate's degree",
    "Bachelor's degree",
    "Master's degree",
    "Professional degree",
    "Doctorate",
    "Prefer not to say",
]


RACE_OPTIONS = [
    "White",
    "Black or African American",
    "American Indian or Alaska Native",
    "Asian",
    "Native Hawaiian or Other Pacific Islander",
    "Prefer not to say",
    "Not listed (please specify)",
]


EMAIL_CLIENT_OPTIONS = [
    "Outlook",
    "Gmail",
    "Apple Mail",
    "Other",
]
