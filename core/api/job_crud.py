from fastapi import APIRouter

from database.models import Job
from database.schemas.job_schema import JobSchemaPOST
from database.schemas.job_schema import JobSchemaPUT
from core.services.queries_service.base_queries import BaseQueries

router = APIRouter(prefix="/job", tags=["Job"])
service = BaseQueries(Job)


@router.get("/{id}/")
async def get_job_by_id(id: int):
    return service.get_by_id(id)


@router.get("/")
async def get_all_jobs():
    return service.get_all_with_relations()


@router.post("/add/")
async def add_job(schema: JobSchemaPOST):
    return service.post_record(schema)


@router.put("/edit/")
async def edit_job(schema: JobSchemaPUT):
    return service.update_record(schema)


@router.delete("/delete/")
async def delete_job(id: int):
    return service.delete_record(id)
