from fastapi import APIRouter
from pydantic import BaseModel
from app.services.search_service import search_query

router = APIRouter()

class QueryIn(BaseModel):
    query: str

@router.post("/")
def run_search(data: QueryIn):
    return search_query(data.query)
