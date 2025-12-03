from fastapi import APIRouter

from database.models import CompanyAccount
from database.schemas.company_account_schema import CompanyAccountSchemaPUT
from database.schemas.company_account_schema import CompanyAccountSchemaPOST
from core.services.queries_service.base_queries import BaseQueries

router = APIRouter(prefix="/company_account", tags=["Company-Accounts"])
service = BaseQueries(CompanyAccount)


@router.get("/{id}/")
async def get_company_account_by_id(id: int):
    return service.get_by_id(id)


@router.get("/")
async def get_all_company_accounts():
    return service.get_all_with_relations()


@router.post("/add/")
async def add_company_account(schema: CompanyAccountSchemaPOST):
    return service.post_record(schema)


@router.put("/edit/")
async def edit_company_account(schema: CompanyAccountSchemaPUT):
    return service.update_record(schema)


@router.delete("/delete/")
async def delete_company_account(id: int):
    return service.delete_record(id)
