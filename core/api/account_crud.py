from fastapi import APIRouter, HTTPException, Response, Depends,UploadFile, File

from database.models import Account
from database.schemas.account_schema import AccountSchemaPOST
from database.schemas.account_schema import AccountSchemaPUT
from database.schemas.register_schema import RegisterApplicantSchema
from core.services.queries_service.base_queries import BaseQueries
from core.services.file_service.file_storage_service import ImageService
from core.services.auth_service.auth_queries_service import AuthQueries


from core.services.auth_service.auth_config import (
    set_auth_cookie,
    verify_password,
    create_access_token,
    get_current_account,
    COOKIE_NAME
)
from database.schemas.register_schema import RegisterCompanySchema


router = APIRouter(prefix="/account", tags=["Accounts"])
service = BaseQueries(Account)
image_service = ImageService(Account)
auth_service = AuthQueries()


@router.get("/me/")
def read_user_me(response: Response, current_account: Account = Depends(get_current_account)):
    access_token = create_access_token(data={"sub": current_account.email})
    set_auth_cookie(response, access_token)

    return {
        "access_token": access_token,
        "message": "AUTHENTICATED"
    }


@router.get("/{id}/")
async def get_account_by_id(id: int):
    return service.get_by_id(id)


@router.get("/")
async def get_all_accounts():
    return service.get_all_with_relations()


@router.post("/register/company/", status_code=201)
async def register_company(schema: RegisterCompanySchema):
    created = auth_service.register_company(schema)
    return {
        "msg": "Company account created successfully",
        "account_id": created["account_id"],
        "company_id": created["company_id"],
    }


@router.post("/register/user/", status_code=201)
async def register_applicant(schema: RegisterApplicantSchema):
    created = auth_service.register_applicant(schema)
    return {
        "msg": "Applicant account created successfully",
        "account_id": created["account_id"],
        "applicant_id": created["applicant_id"],
    }


@router.post("/login/")
async def login(credentials: AccountSchemaPOST, response: Response):
    account = auth_service.get_account_by_email(credentials.email)
    if not account or not verify_password(credentials.password, account.password):
        raise HTTPException(
            status_code=401, detail="INCORRECT EMAIL OR PASSWORD")

    access_token = create_access_token(data={"sub": account.email})
    set_auth_cookie(response, access_token)

    return {
        "access_token": access_token,
        "message": "LOGIN SUCCESSFULLY"
    }


@router.post("/logout/")
async def logout(response: Response):
    response.delete_cookie(key=COOKIE_NAME)
    return {"message": "LOGOUT SUCCESSFULLY"}


@router.put("/edit/")
async def edit_account(schema: AccountSchemaPUT):
    return service.update_record(schema)


@router.delete("/delete/")
async def delete_account(id: int):
    return service.delete_record(id)

@router.post(
    "/image/{object_id}",
    summary="Upload image for an account",
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
        summary="Return image for an account")
async def get_object_image(object_id: int):
    return image_service.get_object_image(object_id)


@router.delete("/image/delete/{object_id}")
async def delete_object_image(object_id: int):
    return image_service.delete_object_image(object_id)
