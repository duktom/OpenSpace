from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class AccountSchemaGET(BaseModel):
    id: int
    email: str
    # password: str
    type: str | None = None
    creation_date: datetime
    exp_date: datetime
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class AccountSchemaPOST(BaseModel):
    email: str
    password: str


class AccountSchemaPUT(BaseModel):
    id: int
    email: str
    password: str
    type: str | None = None
    is_email_verified: bool
