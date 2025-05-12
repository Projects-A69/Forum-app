from common.auth import get_user_or_raise_401
from fastapi import APIRouter, HTTPException, Header
from services.replies_service import create_replies, vote_replies
from services.category_access_service import has_access
from services.topics_service import lock_topic, get_by_id
from data.models import Reply, ReplyCreate, RepliesHasUsers

replies_router = APIRouter(prefix='/api/replies', tags=['Replies'])


@replies_router.post('/{topic_id}/replies')
def create_reply(reply: ReplyCreate, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if reply.user_id != user.id:
        raise HTTPException(status_code=404, detail="User ID is incorrect")
    topic = get_by_id(reply.topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail='Topic not found')
    category_id = topic.category_id
    if not has_access(user.id, category_id, required_level = 1):
        raise HTTPException(status_code=403, detail="No write access")
    result = create_replies(reply.text, user.id, reply.topic_id)
    if result == 'topic is locked':
        raise HTTPException(status_code=404, detail='Topic is locked')

    return result


@replies_router.post('/replies/{reply_id}/votes')
def vote_reply(vote_reply: RepliesHasUsers, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if vote_reply.users_id != user.id:
        raise HTTPException(status_code=401, detail="User ID is incorrect")
    result = vote_replies(users_id = user.id, replies_id= vote_reply.replies_id, vote_type = vote_reply.vote_type)
    if result == "Reply not found":
        raise HTTPException(status_code=404, detail='Reply not found')
    return vote_replies(users_id = vote_reply.users_id, replies_id=vote_reply.replies_id, vote_type=vote_reply.vote_type)
