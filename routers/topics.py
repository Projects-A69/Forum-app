from fastapi import APIRouter,HTTPException, Header
from data.models import Topics,TopicCreate
from services import topics_service
from services.topics_service import get_all, get_by_id,create_topic
from common.auth import get_user_or_raise_401

topics_router = APIRouter(prefix='/topics')

@topics_router.get('/')
def get_topics(search: str | None = None):
    return get_all(search)

@topics_router.get('/{id}')
def get_topic_by_id(id: int):
    topic = get_by_id(id)
    
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    else:
        return topic
    
    
@topics_router.post('/')
def create_topic_router(topic: TopicCreate,x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    return create_topic(topic,user.id)
    
    



