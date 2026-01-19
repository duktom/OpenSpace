import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from core.services.auth_service.auth_config import get_password_hash
from core.services.queries_service.base_queries import BaseQueries

from database.models import Account, Company, CompanyRecruiter, User
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
        
    def update_account_password_hash(self, account_id: int, new_hash: str) -> None:
        try:
            with db_session_scope(commit=True) as session:
                account = session.query(Account).filter(Account.id == account_id).first()
                if not account:
                    raise HTTPException(status_code=404, detail="Account not found")
        except MissingDatabaseError as e:
            logger.error(f"Database error during update_account_password_hash: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    # Company registration
    def register_company(self, data):
        try:
            with db_session_scope(commit=True) as session:
                # Check email uniqueness
                existing_email = (
                    session.query(Account).filter(Account.email == data.email).first()
                )
                if existing_email:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="An account with this email already exists.",
                    )
                # Check ein uniqueness
                existing_ein = (
                    session.query(Company).filter(Company.ein == data.ein).first()
                )
                if existing_ein:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="An account with this EIN already exists.",
                    )

                # Create Account
                new_account = Account(
                    email=data.email,
                    password=get_password_hash(data.password),
                    type="admin"
                )
                session.add(new_account)
                session.flush()  # To get new_account.id

                # Create Company
                new_company = Company(
                    name=data.name,
                    ein=data.ein,
                    account_id=new_account.id
                )
                session.add(new_company)
                session.flush()  # To get new_company.id
                

                # Link Account as CompanyAdmin
                new_admin = CompanyRecruiter(
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
                status_code=status.HTTP_409_CONFLICT, detail="Unknown integrity error."
            )
        except MissingDatabaseError as e:
            logger.error(f"Database error during register_company: {e}")
            raise HTTPException(status_code=404)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during register_company: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    # Example User registration (not fully implemented)
    def register_user(self, data):
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

                new_user = User(
                    account_id=new_account.id,
                    first_name=data.first_name,
                    last_name=data.last_name,
                    birth_date=getattr(data, 'birth_date', None),
                    # Add other applicant-specific fields here
                )
                session.add(new_user)
                session.flush() 

                return {
                    "account_id": new_account.id,
                    "user_id": getattr(new_user, "id", None),
                }
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Unknown integrity error."
            )

        except MissingDatabaseError as e:
            logger.error(f"Database error during register_user: {e}")
            raise HTTPException(status_code=404)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during register_user: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        
