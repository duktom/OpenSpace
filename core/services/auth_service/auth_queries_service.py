import logging

from fastapi import HTTPException

from core.services.auth_service.auth_config import get_password_hash
from core.services.queries_service.base_queries import BaseQueries

from database.models import Account
from database import db_session_scope
from database import MissingDatabaseError

logger = logging.getLogger(__name__)


class AuthQueries(BaseQueries):

    def __init__(self):
        super().__init__(model=Account)

    def create_account(self, account_data):
        account_data.password = get_password_hash(account_data.password)
        try:
            with db_session_scope(commit=True) as session:
                new_account = self.model(
                    email=account_data.email,
                    password=account_data.password
                )
                session.add(new_account)
                return new_account
        except MissingDatabaseError:
            logger.error("Database for provided object does not exist")
            raise HTTPException(404)

    def get_account_by_email(self, email: str):
        try:
            with db_session_scope(commit=False) as session:
                return session.query(self.model).filter(self.model.email == email).first()
        except MissingDatabaseError:
            logger.error("Database for provided object does not exist")
            raise HTTPException(404)
