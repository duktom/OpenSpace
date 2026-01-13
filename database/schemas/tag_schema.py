from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class TagSchemaGET(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TagSchemaPOST(BaseModel):
    name: str
    description: str


class TagSchemaPUT(BaseModel):
    id: int
    name: str
    description: str
