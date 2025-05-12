from fastapi import APIRouter,HTTPException, Header
from data.models import TopicCreate
from services.topics_service import get_all, get_by_id,create_topic,lock_topic,choose_best_reply
from common.auth import get_user_or_raise_401

topics_router = APIRouter(prefix='/api/topics', tags=['TOPICS'])

@topics_router.get('/')
def get_topics(search: str | None = None, sort: str | None = None):
    if sort not in (None, 'asc', 'desc'):
        raise HTTPException(status_code=400, detail="Invalid sort value. Use 'asc' or 'desc'.")
    return get_all(search, sort)



@topics_router.get('/{id}')
def get_topic_by_id(id: int):
    topic = get_by_id(id)
    
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    else:
        return topic
    
    
@topics_router.post('/')
def create_topic_router(topic: TopicCreate, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    result = create_topic(topic, user.id)

    if result == "category_not_found":
        raise HTTPException(status_code=404, detail="Category not found")
    if result == "category_locked":
        raise HTTPException(status_code=403, detail="This category is locked and cannot accept new topics")
    if result == "no_write_access":
        raise HTTPException(status_code=403, detail="You don't have write access to this category")
    if result == "category_private":
        raise HTTPException(status_code=403, detail="This category is private and you don't have access")

    return result


    
@topics_router.put('/{id}/lock')
def lock_topic_route(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required to lock a topic")
    
    updated_topic = lock_topic(id)

    if updated_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")

    return updated_topic



@topics_router.put('/{topic_id}/best-reply/{reply_id}')
def choose_best_reply_route(topic_id: int, reply_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    result = choose_best_reply(topic_id, reply_id, user.id)

    if result == "topic_not_found":
        raise HTTPException(status_code=404, detail="Topic not found")
    elif result == "not_author":
        raise HTTPException(status_code=403, detail="Only the topic author can choose the best reply.")
    elif result == "reply_not_found":
        raise HTTPException(status_code=404, detail="Reply not found for this topic.")

    return result
