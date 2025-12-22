from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class CompanySchemaGET(BaseModel):
    id: int
    name: str
    description: str
    nip: str | None = None
    creation_date: datetime

    model_config = ConfigDict(from_attributes=True)


class CompanySchemaPOST(BaseModel):
    email: str
    password: str
    name: str
    description: str


class CompanySchemaPUT(BaseModel):
    id: int
    name: str
    description: str
