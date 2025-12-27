from typing import Optional

from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class AddressSchema(BaseModel):
    street: str
    city: str
    postal_code: str
    building_number: str
    apartament_number: Optional[str]


class CompanySchemaGET(BaseModel):
    id: int
    name: str
    description: str
    nip: str | None = None
    creation_date: datetime

    model_config = ConfigDict(from_attributes=True)


class CompanySchemaPUT(BaseModel):
    id: int
    name: str
    description: Optional[str]


class CompanyDetailsSchema(BaseModel):
    name: str
    address: AddressSchema
