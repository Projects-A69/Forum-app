from common.auth import get_user_or_raise_401
from data.models import Message, MessageCreate
from services.messages_service import create_messages, view_get_conversation, view_conversations
from fastapi import APIRouter, HTTPException, Header

messages_router = APIRouter(prefix='/api/messages', tags=['Messages'])


@messages_router.post('/',)
def create_message(message: MessageCreate, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if message.sender_id != user.id:
        raise HTTPException(status_code= 401,detail='Sender ID not found')
    if message.receiver_id != user.id:
        raise HTTPException(status_code= 401,detail='Receiver ID not found')
    return create_messages(message)


@messages_router.get('/users/user_id')
def view_conversation(sender_id: int, receiver_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if user.id not in (sender_id, receiver_id):
        raise HTTPException(status_code=401, detail='Access denied')
    return view_get_conversation(sender_id, receiver_id)


@messages_router.get('/conversations/users')
def view_all_conversations(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if id != user.id:
        raise HTTPException(status_code=401, detail='User not found')
    return view_conversations(id)