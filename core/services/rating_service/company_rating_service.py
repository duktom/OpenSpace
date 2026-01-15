import logging

from fastapi import status
from fastapi import HTTPException

from database.schemas.company_rating_schema import RatingCreate
from database.schemas.company_rating_schema import RatingResponse
from core.services.queries_service.company_rating_queries import CompanyRatingQueriesService

logger = logging.getLogger(__name__)


class RatingService:
    def __init__(self):
        self.queries = CompanyRatingQueriesService()

    def process_company_rating(self, company_id: int, rating_data: RatingCreate, current_account) -> RatingResponse:
        if current_account.type != "applicant":
            logger.warning(f"Account {current_account.id} tried to rate but is not an applicant")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tylko kandydaci mogą wystawiać oceny firmom."
            )

        user = self.queries.get_user_by_account_id(current_account.id)

        existing_rating = self.queries.get_existing_rating(
            company_id=company_id,
            user_id=user.id
        )

        if existing_rating:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Już wystawiłeś ocenę tej firmie."
            )

        result = self.queries.create_rating_entry(
            company_id=company_id,
            user_id=user.id,
            score=rating_data.score
        )

        return result
