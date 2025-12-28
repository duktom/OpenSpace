from typing import Optional

from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict

from database.schemas.company_schema import CompanyJobOffertsSchema


class JobOffertsSchema(BaseModel):
    title: str
    company: CompanyJobOffertsSchema
    payoff: float
    posting_img_link: str

    model_config = ConfigDict(from_attributes=True)


class JobOffertSchema(JobOffertsSchema):
    description: str
    
    model_config = ConfigDict(from_attributes=True)


class JobSchemaGET(JobOffertSchema):
    id: int
    company_id: int
    recruiter_id: int
    posting_img_id: str
    posting_date: datetime
    expiry_date: datetime

    model_config = ConfigDict(from_attributes=True)



class JobSchemaPOST(BaseModel):
    title: str
    description: str


class JobSchemaPUT(BaseModel):
    title: str
    description: str
