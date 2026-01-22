from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

from database import db_session_scope
from database.models import User, Account
from database.schemas.user_schema import UserSchemaGET, UserSchemaPUT

from core.services.auth_service.auth_config import get_current_account
from core.services.queries_service.base_queries import BaseQueries
from core.services.file_service.file_storage_service import ImageService


router = APIRouter(prefix="/user", tags=["Users"])
service = BaseQueries(User)
image_service = ImageService(User)


def _assert_user_owner(current_account: Account, user: User) -> None:
    if user.account_id != current_account.id:
        raise HTTPException(status_code=403, detail="FORBIDDEN")


@router.get("/", response_model=list[UserSchemaGET])
async def get_all_users(current_account: Account = Depends(get_current_account)):
    # Avoid user enumeration: admin-only
    if (current_account.type or "").lower() != "admin":
        raise HTTPException(status_code=403, detail="FORBIDDEN")
    return service.get_all_with_relations()


@router.get("/{id}/", response_model=UserSchemaGET)
async def get_user_by_id(id: int, current_account: Account = Depends(get_current_account)):
    user = service.get_by_id(id)
    if (current_account.type or "").lower() != "admin":
        _assert_user_owner(current_account, user)
    return user


@router.get("/image/{object_id}/", summary="Return image for an User")
async def get_object_image(object_id: int):
    return image_service.get_object_image(object_id)


@router.post("/image/{object_id}/", summary="Upload image for an User")
async def upload_object_image(
    object_id: int,
    file: UploadFile = File(...),
    current_account: Account = Depends(get_current_account),
):
    with db_session_scope(commit=False) as session:
        user = session.query(User).filter(User.id == object_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
        _assert_user_owner(current_account, user)

    return image_service.upload_object_image(object_id, file)


@router.put("/edit/", response_model=UserSchemaGET)
async def edit_user(
    schema: UserSchemaPUT,
    current_account: Account = Depends(get_current_account),
):
    with db_session_scope(commit=True) as session:
        user = session.query(User).filter(User.id == schema.id).first()
        if not user:
            raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
        _assert_user_owner(current_account, user)

        # Allow updating profile fields only
        user.first_name = schema.first_name
        user.last_name = schema.last_name
        user.birth_date = schema.birth_date
        user.description = schema.description

        session.flush()
        session.refresh(user)
        session.expunge(user)
        return user


@router.delete("/delete/", response_model=UserSchemaGET)
async def delete_user(
    id: int,
    current_account: Account = Depends(get_current_account),
):
    with db_session_scope(commit=True) as session:
        user = session.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
        _assert_user_owner(current_account, user)

        session.delete(user)
        session.flush()
        session.expunge(user)
        return user


@router.delete("/image/delete/{object_id}", summary="Delete image for an User")
async def delete_object_image(
    object_id: int,
    current_account: Account = Depends(get_current_account),
):
    with db_session_scope(commit=False) as session:
        user = session.query(User).filter(User.id == object_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
        _assert_user_owner(current_account, user)

    return image_service.delete_object_image(object_id)
