import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from core.services.auth_service.auth_config import get_password_hash
from core.services.queries_service.base_queries import BaseQueries

from database.models import Account, Company, CompanyAdmin, Applicant
from database import db_session_scope
from database import MissingDatabaseError

logger = logging.getLogger(__name__)


class AuthQueries(BaseQueries):

    def __init__(self):
        super().__init__(model=Account)

    # Common helpers
    def get_account_by_email(self, email: str):
        # Generic lookup by email
        try:
            with db_session_scope(commit=False) as session:
                return session.query(Account).filter(Account.email == email).first()
        except MissingDatabaseError as e:
            logger.error(f"Database error during get_account_by_email: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        
    # Company registration
    def register_company(self, data):
        try:
            with db_session_scope() as session:
                # Check email uniqueness
                existing = session.query(Account).filter(Account.email == data.email).first()
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="An account with this email already exists."
                    )
                
                # Create Account
                new_account = Account(
                    email=data.email,
                    password=get_password_hash(data.password),
                    type="recruiter"
                )
                session.add(new_account)
                session.flush()  # To get new_account.id

                # Create Company
                new_company = Company(
                    name=data.name,
                    nip=data.nip,
                    description=getattr(data, 'description', None)
                )
                session.add(new_company)
                session.flush()  # To get new_company.id

                # Link Account as CompanyAdmin
                new_admin = CompanyAdmin(
                    account_id=new_account.id,
                    company_id=new_company.id
                )
                session.add(new_admin)

                return {
                    "account_id": new_account.id,
                    "company_id": new_company.id
                }
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already in use."
            )
        except MissingDatabaseError as e:
            logger.error(f"Database error during register_company: {e}")
            raise HTTPException(status_code=404)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during register_company: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        
    # Example Applicant registration (not fully implemented)
    def register_applicant(self, data):
        try:
            with db_session_scope(commit=True) as session:
                # Check email uniqueness
                existing = (
                    session.query(Account)
                    .filter(Account.email == data.email)
                    .first()
                )
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="An account with this email already exists."
                    )

                new_account = Account(
                    email=data.email,
                    password=get_password_hash(data.password),
                    type="applicant",
                )
                session.add(new_account)
                session.flush()  # To get new_account.id

                new_applicant = Applicant(
                    account_id=new_account.id,
                    name=data.name,
                    surname=data.surname,
                    birth_date=getattr(data, 'birth_date', None),
                    # Add other applicant-specific fields here
                    description=getattr(data, 'description', None),
                )
                session.add(new_applicant)

                return {
                    "account_id": new_account.id,
                    "applicant_id": getattr(new_applicant, "id", None),
                }
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already in use."
            )

        except MissingDatabaseError as e:
            logger.error(f"Database error during register_applicant: {e}")
            raise HTTPException(status_code=404)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during register_applicant: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
