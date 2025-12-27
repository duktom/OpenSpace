from typing import Optional

from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class TagSchemaGET(BaseModel):
    id: int
    name: str
    desc: str
    creation_date: datetime

    model_config = ConfigDict(from_attributes=True)


class TagSchemaPOST(BaseModel):
    name: str
    desc: Optional[str]


class TagSchemaPUT(BaseModel):
    name: str
    desc: Optional[str]
