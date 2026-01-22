from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class JobSchemaGET(BaseModel):
    id: int
    company_id: int
    recruiter_id: int
    title: str
    payoff: float
    description: str
    posting_date: datetime
    expiry_date: datetime | None = None
    posting_img_id: str | None = None
    posting_img_link: str | None = None

    model_config = ConfigDict(from_attributes=True)


class JobSchemaPOST(BaseModel):
    title: str
    description: str
    payoff: float

class JobSchemaPUT(BaseModel):
    title: str
    description: str
    payoff: float | None = None
