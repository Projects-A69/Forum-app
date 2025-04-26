from fastapi import APIRouter
from services.replies_service import create_replies
from data.models import Replies, RepliesCreate
replies_router = APIRouter(prefix='/replies')

@replies_router.post('/create')
def create(reply: RepliesCreate):
    return create_replies(reply.text, reply.user_id, reply.topic_id)