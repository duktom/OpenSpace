from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


class CompanyAddressSchema(BaseModel):
    # na ten czas te pola są str lub None, przynajmniej do moment aż nie będzie podczas logowania możliwosći wypełnienia tych danych
    street: str | None = None
    city: str | None = None
    postal_code: str | None = None
    building_num: str | None = None
    apartment_num: Optional[str] = None


class CompanySchemaGET(BaseModel):
    id: int
    name: str
    ein: str
    address: CompanyAddressSchema
    description: str | None = None
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
