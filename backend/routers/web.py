from fastapi import APIRouter
from backend.services import web_service

router = APIRouter()


@router.get("/search")
def web_search(query: str):
    return web_service.search(query)
