"""Company-context authorization helpers.

Guardrails required:
- Only recruiters for a given company may access company-scoped job endpoints.
- The admin account of that company may access those endpoints as well.

In this data model:
- Company admin: Company.account_id == Account.id and Account.type == 'admin'
- Company recruiter: CompanyRecruiter(account_id, company_id)
"""

from __future__ import annotations

from fastapi import HTTPException

from database import db_session_scope
from database.models import Account, Company, CompanyRecruiter


def assert_company_access(*, current_account: Account, company_id: int) -> Company:
    """Ensure `current_account` may act within `company_id`.

    Returns the Company (useful for downstream logic) or raises HTTPException.
    """

    with db_session_scope(commit=False) as session:
        company = session.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="COMPANY_NOT_FOUND")

        # 1) Company admin (single admin per company)
        if (current_account.type or "").lower() == "admin":
            if company.account_id and company.account_id == current_account.id:
                return company

            raise HTTPException(status_code=403, detail="FORBIDDEN_COMPANY_MISMATCH")

        # 2) Recruiter link
        link = (
            session.query(CompanyRecruiter)
            .filter(
                CompanyRecruiter.company_id == company_id,
                CompanyRecruiter.account_id == current_account.id,
            )
            .first()
        )
        if link:
            return company

    raise HTTPException(status_code=403, detail="FORBIDDEN")


def assert_company_admin(*, current_account: Account, company_id: int) -> Company:
    """Company admin only."""

    with db_session_scope(commit=False) as session:
        company = session.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="COMPANY_NOT_FOUND")

        if (current_account.type or "").lower() != "admin":
            raise HTTPException(status_code=403, detail="FORBIDDEN")

        if not company.account_id or company.account_id != current_account.id:
            raise HTTPException(status_code=403, detail="FORBIDDEN_COMPANY_MISMATCH")

        return company


def assert_job_company_match(*, job_company_id: int, request_company_id: int) -> None:
    """Prevent tampering by ensuring a request cannot move a Job across companies."""
    if job_company_id != request_company_id:
        raise HTTPException(status_code=403, detail="FORBIDDEN_COMPANY_MISMATCH")
