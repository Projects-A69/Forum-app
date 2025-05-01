
from common.auth import get_user_or_raise_401
from services.users_service import find_by_username
from data.models import Message, MessageCreate
from services.messages_service import create_message, view_conversation, view_conversations
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from routers.categories import categories_router

messages_router = APIRouter(prefix='/messages', tags=['Messages'])

@messages_router.post('/',)
def create(message: MessageCreate, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if message.sender_id != user.id:
        raise HTTPException(status_code= 401, detail='Sender ID not found')
    if message.receiver_id != user.id:
        raise HTTPException(status_code= 401, detail='Receiver ID not found')


@messages_router.get('/users/user_id')
def view(sender_id: int, receiver_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if sender_id != user.id:
        raise HTTPException(status_code=401, detail='Sender ID not found')
    if receiver_id != user.id:
        raise HTTPException(status_code=401, detail='Receiver ID not found')
    return view_conversation(sender_id, receiver_id)

@messages_router.get('/conversations/users')
def view_all_conversations(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if id != user.id:
        raise HTTPException(status_code=401, detail='User not found')
    return view_conversations(id)