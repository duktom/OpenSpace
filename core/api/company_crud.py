from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from core.services.auth_service.auth_config import get_current_account
from core.services.auth_service.company_access import assert_company_admin
from database import db_session_scope
from database.models import Company, Account
from database.schemas.company_schema import CompanySchemaGET
from database.schemas.company_schema import CompanySchemaPUT
from core.services.queries_service.base_queries import BaseQueries
from core.services.file_service.file_storage_service import ImageService
from core.services.recruiter_service.recruiter_service import RecruiterService

router = APIRouter(prefix="/company", tags=["Company"])
service = BaseQueries(Company)
image_service = ImageService(Company)
recruiter_service = RecruiterService()


@router.get("/", response_model=list[CompanySchemaGET])
async def get_all_companies():
    return service.get_all_with_relations()


@router.get("/profile/{id}/", response_model=CompanySchemaGET)
async def get_company_by_id(id: int):
    return service.get_by_id(id)


@router.get("/image/{object_id}/", summary="Return image for a Company")
async def get_object_image(object_id: int,):
    return image_service.get_object_image(object_id)


@router.post("/image/{object_id}/", summary="Upload image for a Company")
async def upload_object_image(
    object_id: int,
    file: UploadFile = File(...),
    current_account: Account = Depends(get_current_account),
):
    assert_company_admin(current_account=current_account, company_id=object_id)
    return image_service.upload_object_image(object_id, file)


@router.put("/edit/")
async def edit_company(
    schema: CompanySchemaPUT,
    current_account: Account = Depends(get_current_account),
):
    assert_company_admin(current_account=current_account, company_id=schema.id)
    with db_session_scope(commit=True) as session:
        company = session.query(Company).filter(Company.id == schema.id).first()
        if not company:
            raise HTTPException(status_code=404, detail="COMPANY_NOT_FOUND")

        company.name = schema.name
        company.description = schema.description

        session.flush()
        session.refresh(company)
        session.expunge(company)
        return company


@router.delete("/delete/")
async def delete_company(
    id: int,
    current_account: Account = Depends(get_current_account),
):
    assert_company_admin(current_account=current_account, company_id=id)
    return service.delete_record(id)


@router.delete("/image/delete/{object_id}/", summary="Delete image for a Company")
async def delete_object_image(
    object_id: int,
    current_account: Account = Depends(get_current_account),
):
    assert_company_admin(current_account=current_account, company_id=object_id)
    return image_service.delete_object_image(object_id)


@router.get("/search-applicants")
async def search_applicants_by_email(
    mail: str,
    current_account: Account = Depends(get_current_account),
):
    if (current_account.type or "").lower() != "admin":
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    return recruiter_service.search_accounts_by_email(mail)


@router.post("/{company_id}/recruiters/{account_id}/", summary="Assign user account to company (admin-only)")
async def add_user_to_company_recruiter(
    company_id: int,
    account_id: int,
    current_account: Account = Depends(get_current_account),
):
    # Admin check (company ownership is enforced in the service via Company.account_id)
    if (current_account.type or "").lower() != "admin":
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    return recruiter_service.add_user_to_company_recruiters(
        company_id=company_id,
        user_account_id=account_id,
        current_account=current_account,
    )


@router.get("/{company_id}/recruiters/", summary="List user accounts assigned to company (admin-only)")
async def list_company_recruiters(
    company_id: int,
    current_account: Account = Depends(get_current_account),
):
    if (current_account.type or "").lower() != "admin":
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    return recruiter_service.list_company_users(
        company_id=company_id,
        current_account=current_account,
    )


@router.delete("/{company_id}/recruiters/{account_id}/", summary="Remove user account from company (admin-only)")
async def remove_user_from_company_recruiter(
    company_id: int,
    account_id: int,
    current_account: Account = Depends(get_current_account),
):
    if (current_account.type or "").lower() != "admin":
        raise HTTPException(status_code=403, detail="FORBIDDEN")

    return recruiter_service.remove_user_from_company_recruiters(
        company_id=company_id,
        user_account_id=account_id,
        current_account=current_account,
    )
