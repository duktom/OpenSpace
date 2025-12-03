from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class AccountSchemaGET(BaseModel):
    id: int
    email: str
    password: str
    type: bool
    creation_time: datetime
    expiry_date: datetime
    is_email_verified: bool

    model_config = ConfigDict(from_attributes=True)


class AccountSchemaPOST(BaseModel):
    email: str
    password: str
    type: bool
    is_email_verified: bool


class AccountSchemaPUT(BaseModel):
    id: int
    email: str
    password: str
    type: bool
    is_email_verified: bool
