from typing import Optional

from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class CompanyAddressSchema(BaseModel):
    street: str
    city: str
    postal_code: str
    building_num: str
    apartment_num: Optional[str] = None


class CompanySchemaGET(BaseModel):
    id: int
    name: str
    ein: str 
    address: CompanyAddressSchema
    description: str | None = None
    creation_date: Optional[datetime] = None
    profile_img_id: str | None = None
    profile_img_link: str | None = None

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
