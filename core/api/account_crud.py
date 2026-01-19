from fastapi import APIRouter, HTTPException, Response, Depends

from database.models import Account
from database.schemas.account_schema import AccountMeSchemaGET, AccountSchemaGET
from database.schemas.account_schema import AccountSchemaPOST
from database.schemas.account_schema import AccountSchemaPUT
from database.schemas.register_schema import RegisterUserSchema
from core.services.queries_service.base_queries import BaseQueries

from core.services.auth_service.auth_queries_service import AuthQueries

from core.services.auth_service.auth_config import (
    set_auth_cookie,
    verify_password,
    create_access_token,
    get_current_account,
    COOKIE_NAME,
    needs_rehash,
    hash_password,
)
from database.schemas.register_schema import RegisterCompanySchema


router = APIRouter(prefix="/account", tags=["Accounts"])
service = BaseQueries(Account)
auth_service = AuthQueries()


@router.get("/", response_model=list[AccountSchemaGET])
async def get_all_accounts():
    return service.get_all()


@router.get("/me/", response_model=AccountMeSchemaGET)
def read_user_me(response: Response, current_account: Account = Depends(get_current_account)):
    access_token = create_access_token(data={"sub": current_account.email})
    set_auth_cookie(response, access_token)

    return {
        "access_token": access_token,
        "message": "AUTHENTICATED"
    }


@router.get("/{id}/", response_model=AccountSchemaGET)
async def get_account_by_id(id: int):
    return service.get_by_id(id)


@router.post("/login/")
async def login(credentials: AccountSchemaPOST, response: Response):
    account = auth_service.get_account_by_email(credentials.email)
    if not account or not verify_password(credentials.password, account.password):
        raise HTTPException(
            status_code=401, detail="INCORRECT EMAIL OR PASSWORD")

    if needs_rehash(account.password):
        new_hash = hash_password(credentials.password)
        auth_service.update_account_password_hash(account.id, new_hash)

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


@router.post("/register/company/", status_code=201)
async def register_company(schema: RegisterCompanySchema):
    created = auth_service.register_company(schema)
    return {
        "msg": "Company account created successfully",
        "account_id": created["account_id"],
        "company_id": created["company_id"],
    }


@router.post("/register/user/", status_code=201)
async def register_user(schema: RegisterUserSchema):
    created = auth_service.register_user(schema)
    return {
        "msg": "User account created successfully",
        "account_id": created["account_id"],
        "user_id": created["user_id"],
    }


@router.put("/edit/")
async def edit_account(schema: AccountSchemaPUT):
    return service.update_record(schema)


@router.delete("/delete/")
async def delete_account(id: int):
    return service.delete_record(id)
