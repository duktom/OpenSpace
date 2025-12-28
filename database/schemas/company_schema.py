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


class CompanyJobOffertsSchema(BaseModel):
    name: str
    address: CompanyAddressSchema


class CompanyProfilesSchema(BaseModel):
    name: str
    creation_date: datetime
    profile_img_link: str


class CompanyProfileSchema(CompanyJobOffertsSchema):
    creation_date: datetime
    description: str
    profile_img_link: str
    

class CompanySchemaGET(BaseModel):
    id: int
    name: str
    ein: str | None = None
    address: CompanyAddressSchema
    description: str
    creation_date: datetime
    profile_img_id: str
    profile_img_link: str

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
