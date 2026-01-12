import logging
from fastapi import HTTPException, UploadFile, File
from sqlalchemy.sql import exists
from database import db_session_scope
from database.models import Account, Company, CompanyRecruiter
logger = logging.getLogger(__name__)


class RecruiterService:
    def _assert_admin_and_company_match(self, current_account: Account, company_id: int) -> Company:
        # 1) Admin check
        if (current_account.type or "").lower() != "admin":
            raise HTTPException(status_code=403, detail="FORBIDDEN")

        with db_session_scope(commit=False) as session:
            company = session.query(Company).filter(Company.id == company_id).first()
            if not company:
                raise HTTPException(status_code=404, detail="COMPANY_NOT_FOUND")

            # 2) Company ownership check (single admin per company)
            if not company.account_id or company.account_id != current_account.id:
                raise HTTPException(status_code=403, detail="FORBIDDEN_COMPANY_MISMATCH")

            return company

    def search_accounts_by_email(self, mail: str) -> list[Account]:
        with db_session_scope(commit=False) as session:
            return (
                session.query(Account)
                .filter(
                    Account.email.like(f"%{mail}%"),
                    Account.type == "applicant",
                )
                .all()
            )
        
    def add_applicant_to_company_recruiters(self, company_id: int, applicant_account_id: int, current_account: Account) -> dict:
        self._assert_admin_and_company_match(current_account, company_id)

        with db_session_scope(commit=True) as session:
            applicant = session.query(Account).filter(Account.id == applicant_account_id).first()
            if not applicant:
                raise HTTPException(status_code=404, detail="ACCOUNT_NOT_FOUND")
            if (applicant.type or "").lower() != "applicant":
                raise HTTPException(status_code=400, detail="ACCOUNT_NOT_APPLICANT")

            already = session.query(
                exists().where(
                    (CompanyRecruiter.account_id == applicant_account_id) &
                    (CompanyRecruiter.company_id == company_id)
                )
            ).scalar()
            if already:
                return {"status": "ok", "detail": "ALREADY_ASSIGNED", "company_id": company_id, "account_id": applicant_account_id}

            link = CompanyRecruiter(account_id=applicant_account_id, company_id=company_id)
            session.add(link)
            return {"status": "ok", "detail": "ASSIGNED", "company_id": company_id, "account_id": applicant_account_id}

    def list_company_applicants(self, company_id: int, current_account: Account) -> list[Account]:
        self._assert_admin_and_company_match(current_account, company_id)

        with db_session_scope(commit=False) as session:
            return (
                session.query(Account)
                .join(CompanyRecruiter, CompanyRecruiter.account_id == Account.id)
                .filter(
                    CompanyRecruiter.company_id == company_id,
                    Account.type == "applicant",
                )
                .all()
            )

    def remove_applicant_from_company_recruiters(self, company_id: int, applicant_account_id: int, current_account: Account) -> dict:
        self._assert_admin_and_company_match(current_account, company_id)

        with db_session_scope(commit=True) as session:
            link = (
                session.query(CompanyRecruiter)
                .filter(
                    CompanyRecruiter.company_id == company_id,
                    CompanyRecruiter.account_id == applicant_account_id,
                )
                .first()
            )
            if not link:
                raise HTTPException(status_code=404, detail="ASSIGNMENT_NOT_FOUND")

            session.delete(link)
            return {"status": "ok", "detail": "REMOVED", "company_id": company_id, "account_id": applicant_account_id}