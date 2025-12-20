from pydantic import BaseModel


# class CompanyAccountSchemaGET(BaseModel):
#     id: int
#     account_id: int
#     company_id: int
#     recruter_name: str
#     recruter_surname: str
#     recruter_desc: str


# class CompanyAccountSchemaPOST(BaseModel):
#     recruter_name: str
#     recruter_surname: str
#     recruter_desc: str


# class CompanyAccountSchemaPUT(BaseModel):
#     recruter_name: str
#     recruter_surname: str
#     recruter_desc: str

class CompanyAccountSchemaGET(BaseModel):
    id: int
    account_id: int
    company_id: int

