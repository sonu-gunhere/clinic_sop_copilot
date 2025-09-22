from fastapi import APIRouter
from backend.services import cite_service

router = APIRouter()


@router.post("/validate")
def validate(text: str, citations: list[str]):
    return cite_service.validate(text, citations)
