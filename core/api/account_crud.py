from fastapi import APIRouter

from database.models import Account
from database.schemas.account_schema import AccountSchemaPOST
from database.schemas.account_schema import AccountSchemaPUT
from core.services.queries_service.base_queries import BaseQueries

router = APIRouter(prefix="/accounts", tags=["Accounts"])
service = BaseQueries(Account)


@router.get("/{id}/")
async def get_account_by_id(id: int):
    return service.get_by_id(id)


@router.get("/")
async def get_all_accounts():
    return service.get_all_with_relations()


@router.post("/add/")
async def add_account(schema: AccountSchemaPOST):
    return service.post_record(schema)


@router.put("/edit/")
async def edit_account(schema: AccountSchemaPUT):
    return service.update_record(schema)


@router.delete("/delete/")
async def delete_account(id: int):
    return service.delete_record(id)
