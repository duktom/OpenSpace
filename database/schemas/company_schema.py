from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class CompanySchemaGET(BaseModel):
    id: int
    name: str
    desc: str
    creation_date: datetime

    model_config = ConfigDict(from_attributes=True)


class CompanySchemaPOST(BaseModel):
    name: str
    desc: str


class CompanySchemaPUT(BaseModel):
    name: str
    desc: str
