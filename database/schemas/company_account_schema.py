from pydantic import BaseModel


class CompanyAccountSchemaGET(BaseModel):
    id: int
    account_id: int
    company_id: int
