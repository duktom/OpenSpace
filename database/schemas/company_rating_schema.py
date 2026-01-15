from pydantic import BaseModel, Field


class RatingCreate(BaseModel):
    score: int = Field(..., ge=1, le=5)


class RatingResponse(BaseModel):
    company_id: int
    rating: float
    ratings_count: int
