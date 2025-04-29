from fastapi import APIRouter
from services.replies_service import create_replies, vote_replies, get_vote_reply
from data.models import Replies, RepliesCreate, RepliesHasUsers
replies_router = APIRouter(prefix='/replies')

@replies_router.post('/create')
def create(reply: RepliesCreate):
    return create_replies(reply.text, reply.user_id, reply.topic_id)

@replies_router.post('/votes')
def vote_reply(vote_reply: RepliesHasUsers):
    return vote_replies(users_id = vote_reply.users_id, replies_id=vote_reply.replies_id, vote_type=vote_reply.vote_type)

@replies_router.get('/replies/{replies_id}')
def get_vote(replies_id: int):
    return get_vote_reply(replies_id)