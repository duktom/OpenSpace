from datetime import date

from pydantic import BaseModel, ConfigDict


class ApplicantSchemaGET(BaseModel):
    id: int
    account_id: int
    name: str
    surname: str
    birth_date: date
    description: str

    model_config = ConfigDict(from_attributes=True)


class ApplicantSchemaPOST(BaseModel):
    name: str
    surname: str
    birth_date: date
    description: str


class ApplicantSchemaPUT(BaseModel):
    id: int
    name: str
    surname: str
    birth_date: date
    description: str
