from datetime import date

from pydantic import BaseModel, ConfigDict


class ApplicantSchemaGET(BaseModel):
    id: int
    account_id: int
    first_name: str
    last_name: str
    birth_date: date
    description: str

    model_config = ConfigDict(from_attributes=True)


class ApplicantSchemaPOST(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    description: str


class ApplicantSchemaPUT(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: date
    description: str
