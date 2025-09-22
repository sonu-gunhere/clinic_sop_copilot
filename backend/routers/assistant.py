from fastapi import APIRouter, Query
from backend.services import orchestrator

router = APIRouter()


@router.get("/ask")
def ask(query: str = Query(..., description="User clinical SOP question")):
    return orchestrator.generate_answer(query)
