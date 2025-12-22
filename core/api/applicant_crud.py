from fastapi import APIRouter

from database.models import Applicant
from database.schemas.applicant_schema import ApplicantSchemaPUT
from core.services.queries_service.base_queries import BaseQueries

router = APIRouter(prefix="/applicant", tags=["Applicants"])
service = BaseQueries(Applicant)


@router.get("/{id}/")
async def get_aaplicant_by_id(id: int):
    return service.get_by_id(id)


@router.get("/")
async def get_all_applicants():
    return service.get_all_with_relations()


@router.put("/edit/")
async def edit_applicant(schema: ApplicantSchemaPUT):
    return service.update_record(schema)


@router.delete("/delete/")
async def delete_applicant(id: int):
    return service.delete_record(id)
