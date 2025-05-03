from common.auth import get_user_or_raise_401
from fastapi import APIRouter, HTTPException, Header
from services.replies_service import create_replies, vote_replies
from services.topics_service import lock_topic, get_by_id
from data.models import Reply, ReplyCreate, RepliesHasUsers

replies_router = APIRouter(prefix='/replies', tags=['Replies'])


@replies_router.post('/{topic_id}/replies')
def create_reply(reply: ReplyCreate, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    topic_locked = lock_topic(reply.topic_id)
    topic = get_by_id(reply.topic_id)
    if topic is True:
        raise HTTPException(status_code = 403, detail = "This topic is locked")
    if topic is None:
        raise HTTPException(status_code = 404, detail = "This topic does not exist")
    return create_replies(reply.text, reply.user_id, reply.topic_id)


@replies_router.post('/replies/{reply_id}/votes')
def vote_reply(vote_reply: RepliesHasUsers, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    topic = get_by_id(reply.topic_id)
    if topic is None:
        raise HTTPException(status_code = 404, detail = "This topic does not exist")
    return vote_replies(users_id = vote_reply.users_id, replies_id=vote_reply.replies_id, vote_type=vote_reply.vote_type)
