from fastapi import APIRouter, UploadFile, File

from database.models import Applicant
from database.schemas.applicant_schema import ApplicantSchemaGET
from database.schemas.applicant_schema import ApplicantSchemaPUT
from core.services.queries_service.base_queries import BaseQueries
from core.services.file_service.file_storage_service import ImageService

router = APIRouter(prefix="/applicant", tags=["Applicants"])
service = BaseQueries(Applicant)
image_service = ImageService(Applicant)


@router.get("/", response_model=list[ApplicantSchemaGET])
async def get_all_applicants():
    return service.get_all_with_relations()


@router.get("/{id}/", response_model=ApplicantSchemaGET)
async def get_aaplicant_by_id(id: int):
    return service.get_by_id(id)


@router.get("/image/{object_id}", summary="Return image for an Applicant")
async def get_object_image(object_id: int):
    return image_service.get_object_image(object_id)


@router.post("/image/{object_id}", summary="Upload image for an Applicant")
async def upload_object_image(object_id: int, file: UploadFile = File(...)):
    return image_service.upload_object_image(object_id, file)


@router.put("/edit/")
async def edit_applicant(schema: ApplicantSchemaPUT):
    return service.update_record(schema)


@router.delete("/delete/")
async def delete_applicant(id: int):
    return service.delete_record(id)


@router.delete("/image/delete/{object_id}", summary="Delete image for an Applicant")
async def delete_object_image(object_id: int):
    return image_service.delete_object_image(object_id)
