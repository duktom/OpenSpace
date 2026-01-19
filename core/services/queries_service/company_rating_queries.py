import logging

from fastapi import HTTPException

from database import db_session_scope
from database import MissingDatabaseError

from database.models import User, CompanyRating, Company
from .base_queries import BaseQueries

logger = logging.getLogger(__name__)


class CompanyRatingQueriesService(BaseQueries):
    def __init__(self):
        super().__init__(model=User)

    def get_user_by_account_id(self, account_id: int):
        try:
            with db_session_scope(commit=False) as session:
                result = session.query(self.model).filter(
                    self.model.account_id == account_id).first()

                if result is None:
                    raise HTTPException(status_code=404, detail="User not found")
                return result
        except MissingDatabaseError:
            logger.error("Database for provided object does not exist")
            raise HTTPException(404)

    def get_existing_rating(self, company_id: int, user_id: int):
        try:
            with db_session_scope(commit=False) as session:
                return session.query(CompanyRating).filter(
                    CompanyRating.company_id == company_id,
                    CompanyRating.user_id == user_id
                ).first()
        except MissingDatabaseError:
            raise HTTPException(500)

    def create_rating_entry(self, company_id: int, user_id: int, score: int):
        try:
            with db_session_scope(commit=True) as session:
                new_rating = CompanyRating(
                    company_id=company_id,
                    user_id=user_id,
                    score=score
                )
                session.add(new_rating)

                company = session.query(Company).filter(Company.id == company_id).first()
                if not company:
                    raise HTTPException(status_code=404, detail="Company not found")

                old_count = company.ratings_count or 0
                old_avg = company.rating or 0

                new_count = old_count + 1
                new_avg = ((old_avg * old_count) + score) / new_count

                company.ratings_count = new_count
                company.rating = new_avg

                return {
                    "company_id": company_id,
                    "rating": round(new_avg, 2),
                    "ratings_count": new_count
                }
        except Exception as e:
            logger.error(f"Error while creating rating: {e}")
            raise HTTPException(status_code=400, detail="Could not submit rating")
