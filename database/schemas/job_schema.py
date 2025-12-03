from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class JobSchemaGET(BaseModel):
    id: int
    name: str
    desc: str
    creation_date: datetime
    company_id: int
    exp_date: datetime

    model_config = ConfigDict(from_attributes=True)


class JobSchemaPOST(BaseModel):
    name: str
    desc: str


class JobSchemaPUT(BaseModel):
    name: str
    desc: str
