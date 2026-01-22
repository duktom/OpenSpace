from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

from database import db_session_scope
from database.models import Job, Account
from database.schemas.job_schema import JobSchemaGET, JobSchemaPOST, JobSchemaPUT

from core.services.auth_service.auth_config import get_current_account
from core.services.auth_service.company_access import assert_company_access
from core.services.queries_service.base_queries import BaseQueries
from core.services.file_service.file_storage_service import ImageService


router = APIRouter(prefix="/job", tags=["Job"])

# Public read service
service = BaseQueries(Job)
image_service = ImageService(Job)


@router.get("/", response_model=list[JobSchemaGET])
async def get_all_jobs():
    return service.get_all_with_relations()


@router.get("/{id}/", response_model=JobSchemaGET)
async def get_job_by_id(id: int):
    return service.get_by_id(id)


@router.get("/image/{object_id}", summary="Return image for Job posting")
async def get_object_image(object_id: int):
    return image_service.get_object_image(object_id)


# =====================
# Secured mutating routes
# =====================


@router.post("/add/", response_model=JobSchemaGET)
async def add_job(
    schema: JobSchemaPOST,
    current_account: Account = Depends(get_current_account),
):
    # Only recruiters for company OR company admin may create jobs for that company.
    assert_company_access(current_account=current_account, company_id=schema.company_id)

    with db_session_scope(commit=True) as session:
        new_job = Job(**schema.model_dump())
        session.add(new_job)
        session.flush()
        session.refresh(new_job)
        session.expunge(new_job)
        return new_job


@router.put("/edit/", response_model=JobSchemaGET)
async def edit_job(
    schema: JobSchemaPUT,
    current_account: Account = Depends(get_current_account),
):
    with db_session_scope(commit=True) as session:
        job = session.query(Job).filter(Job.id == schema.id).first()
        if not job:
            raise HTTPException(status_code=404, detail="JOB_NOT_FOUND")

        assert_company_access(current_account=current_account, company_id=job.company_id)

        data = schema.model_dump(exclude_unset=True)
        # Disallow changing job.id and company_id through this endpoint
        data.pop("id", None)
        data.pop("company_id", None)

        for k, v in data.items():
            setattr(job, k, v)

        session.flush()
        session.refresh(job)
        session.expunge(job)
        return job


@router.delete("/delete/", response_model=JobSchemaGET)
async def delete_job(
    id: int,
    current_account: Account = Depends(get_current_account),
):
    with db_session_scope(commit=True) as session:
        job = session.query(Job).filter(Job.id == id).first()
        if not job:
            raise HTTPException(status_code=404, detail="JOB_NOT_FOUND")

        assert_company_access(current_account=current_account, company_id=job.company_id)
        session.delete(job)
        session.flush()
        session.expunge(job)
        return job


@router.post("/image/{object_id}", summary="Upload image for Job posting")
async def upload_object_image(
    object_id: int,
    file: UploadFile = File(...),
    current_account: Account = Depends(get_current_account),
):
    # Enforce company context based on the job being modified
    with db_session_scope(commit=False) as session:
        job = session.query(Job).filter(Job.id == object_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="JOB_NOT_FOUND")
        assert_company_access(current_account=current_account, company_id=job.company_id)

    return image_service.upload_object_image(object_id, file)


@router.delete("/image/delete/{object_id}")
async def delete_object_image(
    object_id: int,
    current_account: Account = Depends(get_current_account),
):
    with db_session_scope(commit=False) as session:
        job = session.query(Job).filter(Job.id == object_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="JOB_NOT_FOUND")
        assert_company_access(current_account=current_account, company_id=job.company_id)

    return image_service.delete_object_image(object_id)
