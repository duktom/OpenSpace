from datetime import date
from pydantic import BaseModel, EmailStr, Field


class RegisterCompanySchema(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=50,
        description="Password must be between 8 and 128 characters long."
    )
    name: str = Field(min_length=2, max_length=50, pattern="^[a-zA-ZĄĆĘŁŃÓŚŹŻąćęłńóśźż ]+$")
    # Add Ein field for company identification number
    ein: str = Field(
        pattern=r"^\d{10}$",
        description="EIN must be exactly 10 characters long."
    )


class RegisterUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=50,
        description="Password must be between 8 and 128 characters long."
    )
    first_name: str = Field(min_length=2, max_length=30, pattern="^[a-zA-ZĄĆĘŁŃÓŚŹŻąćęłńóśźż ]+$")
    last_name: str = Field(min_length=2, max_length=30, pattern="^[a-zA-ZĄĆĘŁŃÓŚŹŻąćęłńóśźż ]+$")

    birth_date: date | None = None
