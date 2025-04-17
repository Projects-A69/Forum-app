from fastapi import APIRouter
from services.topics_service import get_all

topics_router = APIRouter(prefix='/topics')

@topics_router.get('/')
def get_topics(search: str | None = None):
    return get_all(search)


