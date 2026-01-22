from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class JobSchemaGET(BaseModel):
    id: int
    company_id: int
    title: str
    payoff: float
    description: str
    posting_date: datetime
    expiry_date: datetime | None = None
    posting_img_id: str | None = None
    posting_img_link: str | None = None

    model_config = ConfigDict(from_attributes=True)


class JobSchemaPOST(BaseModel):
    company_id: int
    title: str
    description: str
    payoff: float
    expiry_date: datetime | None = None

class JobSchemaPUT(BaseModel):
    id: int
    title: str | None = None
    description: str | None = None
    payoff: float | None = None
    expiry_date: datetime | None = None
