from fastapi import APIRouter

from database.models import Company
from database.schemas.company_schema import CompanySchemaPUT
from database.schemas.company_schema import CompanySchemaPOST
from core.services.queries_service.base_queries import BaseQueries

router = APIRouter(prefix="/company", tags=["Company"])
service = BaseQueries(Company)


@router.get("/{id}/")
async def get_company_by_id(id: int):
    return service.get_by_id(id)


@router.get("/")
async def get_all_companies():
    return service.get_all_with_relations()


@router.post("/add/")
async def add_company(schema: CompanySchemaPOST):
    return service.post_record(schema)


@router.put("/edit/")
async def edit_company(schema: CompanySchemaPUT):
    return service.update_record(schema)


@router.delete("/delete/")
async def delete_company(id: int):
    return service.delete_record(id)
