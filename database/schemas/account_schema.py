from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional

from database.schemas.user_schema import UserSchemaGET
from database.schemas.company_schema import CompanySchemaGET


class AccountSchemaGET(BaseModel):
    id: int
    email: str
    type: str | None = None
    created_at: datetime
    exp_date: datetime | None = None
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class AccountMeSchemaGET(BaseModel):
    access_token: str
    message: str
    account_id: int
    account_type: str | None = None
    user: Optional[UserSchemaGET] = None
    company: Optional[CompanySchemaGET] = None


class AccountSchemaPOST(BaseModel):
    email: str
    password: str


class AccountSchemaPUT(BaseModel):
    id: int
    email: str | None = None
    password: str | None = None
    # Admin-managed fields kept optional for compatibility; they are ignored in /account/edit/
    type: str | None = None
    is_verified: bool | None = None
