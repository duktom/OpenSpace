from datetime import datetime

from pydantic import BaseModel


class ApplicantSchemaGET(BaseModel):
    id: int
    account_id: int
    name: str
    surname: str
    birth_date: datetime
    desc: str


class ApplicantSchemaPOST(BaseModel):
    name: str
    surname: str
    birth_date: datetime
    desc: str


class ApplicantSchemaPUT(BaseModel):
    name: str
    surname: str
    birth_date: datetime
    desc: str
