from fastapi import APIRouter,UploadFile, File

from database.models import Company
from database.schemas.company_schema import CompanySchemaPUT
from database.schemas.company_schema import CompanySchemaPOST
from core.services.queries_service.base_queries import BaseQueries
from core.services.file_service.file_storage_service import ImageService



router = APIRouter(prefix="/company", tags=["Company"])
service = BaseQueries(Company)
image_service = ImageService(Company)

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

@router.post(
    "/image/{object_id}",
    summary="Upload image for Company",
)
async def upload_object_image(
    object_id: int,
    file: UploadFile = File(...)
):
    return image_service.upload_object_image(
        object_id,
        file
    )

@router.get(
        "/image/{object_id}",
        summary="Return image for company",)
async def get_object_image(object_id: int,):
    return image_service.get_object_image(object_id)

@router.delete("/image/delete/{object_id}")
async def delete_object_image(object_id: int):
    return image_service.delete_object_image(object_id)