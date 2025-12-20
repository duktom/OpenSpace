from datetime import date
from pydantic import BaseModel, EmailStr, Field

class RegisterCompanySchema(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password must be between 8 and 128 characters long."
    )
    name: str
    # Add Nip field for company identification number
    nip: str = Field(
        min_length=10,
        max_length=10,
        nospace=True,
        nodash=True,
        description="NIP must be exactly 10 characters long."
    )
    description: str | None = None


class RegisterApplicantSchema(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password must be between 8 and 128 characters long."
    )
    name: str = Field(min_length=2, max_length=100)
    surname: str = Field(min_length=2, max_length=100)

    birth_date: date | None = None