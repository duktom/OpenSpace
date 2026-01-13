from datetime import date

from pydantic import BaseModel, ConfigDict


class UserSchemaGET(BaseModel):
    id: int
    account_id: int
    first_name: str
    last_name: str
    birth_date: date
    description: str | None = None
    profile_img_id: str | None = None
    profile_img_link: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserSchemaPOST(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    description: str


class UserSchemaPUT(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: date
    description: str
