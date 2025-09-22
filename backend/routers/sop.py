from fastapi import APIRouter
from backend.services import sop_service

router = APIRouter()

@router.get("/search")
def search_sop(query: str):
    return sop_service.search(query)

@router.get("/read/{section_id}")
def read_sop(section_id: str):
    return sop_service.read(section_id)

