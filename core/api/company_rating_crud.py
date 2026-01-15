from fastapi import Depends
from fastapi import APIRouter

from core.services.auth_service.auth_config import get_current_account

from database.schemas.company_rating_schema import RatingCreate
from database.schemas.company_rating_schema import RatingResponse

from core.services.rating_service.company_rating_service import RatingService

router = APIRouter(prefix="/company_rating", tags=["Ratings"])


@router.post("/{company_id}/", response_model=RatingResponse)
def rate_company(company_id: int,
                 rating_data: RatingCreate,
                 current_account=Depends(get_current_account),
                 service: RatingService = Depends(RatingService)):
    return service.process_company_rating(company_id, rating_data, current_account)
