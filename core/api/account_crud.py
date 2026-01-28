from fastapi import APIRouter, HTTPException, Response, Depends

from database import db_session_scope

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
async def get_all_accounts(
    current_account: Account = Depends(get_current_account)
):
    if current_account.type != "admin":
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    return service.get_all()




@router.get("/me/", response_model=AccountMeSchemaGET)
def read_user_me(response: Response, current_account: Account = Depends(get_current_account)):
    access_token = create_access_token(data={"sub": current_account.email})
    set_auth_cookie(response, access_token)

    return {
        "account_type": current_account.type,
        "access_token": access_token,
        "message": "AUTHENTICATED"
    }


@router.get("/{id}/", response_model=AccountSchemaGET)
async def get_account_by_id(
    id: int,
    current_account: Account = Depends(get_current_account),
):
    # Owner can read own account; admin can read any account
    if (current_account.type or "").lower() != "admin" and current_account.id != id:
        raise HTTPException(status_code=403, detail="FORBIDDEN")
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


@router.put("/edit/", response_model=AccountSchemaGET)
async def edit_account(
    schema: AccountSchemaPUT,
    current_account: Account = Depends(get_current_account),
):
    # Only owner can modify own account
    if current_account.id != schema.id:
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    # Only allow email/password changes via this endpoint
    with db_session_scope(commit=True) as session:
        account = session.query(Account).filter(Account.id == schema.id).first()
        if not account:
            raise HTTPException(status_code=404, detail="ACCOUNT_NOT_FOUND")

        if schema.email:
            account.email = schema.email

        if schema.password:
            account.password = hash_password(schema.password)

        session.flush()
        session.refresh(account)
        session.expunge(account)
        return account


@router.delete("/delete/", response_model=AccountSchemaGET)
async def delete_account(
    id: int,
    current_account: Account = Depends(get_current_account),
):
    # Only owner can delete own account
    if current_account.id != id:
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    with db_session_scope(commit=True) as session:
        account = session.query(Account).filter(Account.id == id).first()
        if not account:
            raise HTTPException(status_code=404, detail="ACCOUNT_NOT_FOUND")
        session.delete(account)
        session.flush()
        session.expunge(account)
        return account
