from fastapi import APIRouter, Query
from core.services.queries_service.search_queries import SearchQueries

router = APIRouter(prefix="/search", tags=["Search"])
service = SearchQueries()

@router.get("/")
async def get_search_results(q: str = Query(..., min_length=1)):
    """
    Endpoint, zwraca wyniki dla osób, ofert i firm.
    """
    return service.global_search(q)
