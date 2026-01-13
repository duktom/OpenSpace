from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


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


class AccountSchemaPOST(BaseModel):
    email: str
    password: str


class AccountSchemaPUT(BaseModel):
    id: int
    email: str
    password: str
    type: str | None = None
    is_verified: bool
