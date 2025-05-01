from common.auth import get_user_or_raise_401
from fastapi import APIRouter, HTTPException, Header
from services.replies_service import create_replies, vote_replies, get_vote_reply
from data.models import Reply, ReplyCreate, RepliesHasUsers
replies_router = APIRouter(prefix='/replies', tags=['Replies'])

@replies_router.post('/{topic_id}/replies')
def create(reply: ReplyCreate, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    return create_replies(reply.text, reply.user_id, reply.topic_id)

@replies_router.post('/replies/{reply_id}/votes')
def vote_reply(vote_reply: RepliesHasUsers, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    return vote_replies(users_id = vote_reply.users_id, replies_id=vote_reply.replies_id, vote_type=vote_reply.vote_type)
