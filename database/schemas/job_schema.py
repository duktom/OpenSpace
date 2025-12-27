from typing import Optional

from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict

from database.schemas.company_schema import CompanyDetailsSchema


class JobSchemaGET(BaseModel):
    id: int
    title: str
    company: CompanyDetailsSchema
    price: float
    description: str
    posting_date: datetime

    model_config = ConfigDict(from_attributes=True)


class JobSchemaPOST(BaseModel):
    title: str
    description: Optional[str]


class JobSchemaPUT(BaseModel):
    title: str
    description: Optional[str]

class JobOffertsSchema(BaseModel):
    title: str
    company: CompanyDetailsSchema
    price: float
    posting_img_link: str
