from fastapi import APIRouter

from database.models import Tag
from database.schemas.tag_schema import TagSchemaPOST
from database.schemas.tag_schema import TagSchemaPUT
from core.services.queries_service.base_queries import BaseQueries

router = APIRouter(prefix="/tags", tags=["Tags"])
service = BaseQueries(Tag)


@router.get("/")
async def get_all_tags():
    return service.get_all_with_relations()


@router.get("/{id}/")
async def get_tag_by_id(id: int):
    return service.get_by_id(id)


@router.post("/add/")
async def add_tag(schema: TagSchemaPOST):
    return service.post_record(schema)


@router.put("/edit/")
async def edit_tag(schema: TagSchemaPUT):
    return service.update_record(schema)


@router.delete("/delete/")
async def delete_tag(id: int):
    return service.delete_record(id)
