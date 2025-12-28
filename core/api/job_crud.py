from fastapi import APIRouter, UploadFile, File

from database.models import Job
from database.schemas.job_schema import JobSchemaGET
from database.schemas.job_schema import JobSchemaPOST
from database.schemas.job_schema import JobSchemaPUT
from core.services.queries_service.base_queries import BaseQueries
from core.services.file_service.file_storage_service import ImageService


router = APIRouter(prefix="/job", tags=["Job"])
service = BaseQueries(Job)
image_service = ImageService(Job)


@router.get("/", response_model=list[JobSchemaGET])
async def get_all_jobs():
    return service.get_all_with_relations()


@router.get("/{id}/", response_model=JobSchemaGET)
async def get_job_by_id(id: int):
    return service.get_by_id(id)


@router.get("/image/{object_id}", summary="Return image for Job posting")
async def get_object_image(object_id: int,):
    return image_service.get_object_image(object_id)


@router.post("/add/")
async def add_job(schema: JobSchemaPOST):
    return service.post_record(schema)


@router.post("/image/{object_id}", summary="Upload image for Job posting")
async def upload_object_image(object_id: int, file: UploadFile = File(...)):
    return image_service.upload_object_image(object_id, file)


@router.put("/edit/")
async def edit_job(schema: JobSchemaPUT):
    return service.update_record(schema)


@router.delete("/delete/")
async def delete_job(id: int):
    return service.delete_record(id)


@router.delete("/image/delete/{object_id}")
async def delete_object_image(object_id: int):
    return image_service.delete_object_image(object_id)
