from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from database import db_session_scope
from database.models import Job, Account
from database.schemas.job_schema import JobSchemaPOST
from core.services.queries_service.base_queries import BaseQueries

class JobQueries(BaseQueries):

    def create_job_for_account(self, schema: JobSchemaPOST, account: Account) -> Job:
        target_company_id = None

            # 1. Sprawdzenie czy to Admin Firmy #
        if account.admin_company:
            target_company_id = account.admin_company.id
            # 2. Sprawdzenie czy to Rekruter #
        elif account.company_recruiters:
            target_company_id = account.company_recruiters[0].company_id
        
            # Jeśli nie znaleziono firmy -> Błąd #
        if not target_company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Company Admins or Recruiters can post jobs."
            )

        try:
            with db_session_scope(commit=True) as session:
                    # Przygotowanie danych #
                job_data = schema.model_dump()
                job_data["company_id"] = target_company_id
                
                    # Tworzenie obiektu #
                new_job = self.model(**job_data)
                session.add(new_job)
                
                session.flush() 
                session.refresh(new_job)
                
                session.expunge(new_job) 
                return new_job
                
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
