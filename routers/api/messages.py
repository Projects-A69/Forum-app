from common.auth import get_user_or_raise_401
from data.models import MessageCreate
from services.messages_service import create_messages, view_get_conversation, view_conversations
from fastapi import APIRouter, HTTPException, Header

messages_router = APIRouter(prefix='/api/messages', tags=['Messages'])


@messages_router.post('/')
def create_message(message: MessageCreate, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if user.id not in (message.sender_id, message.receiver_id):
        raise HTTPException(status_code= 401, detail='User ID does not exist')
    create_messages(message.sender_id, message.receiver_id, message.text)
    return {
        "message": message.text,
        "to_user_id": message.receiver_id
    }

@messages_router.get('/users/{user_id}')
def view_conversation(sender_id: int, receiver_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if user.id not in (sender_id, receiver_id):
        raise HTTPException(status_code=401, detail='Access denied')
    return view_get_conversation(sender_id, receiver_id)


@messages_router.get('/conversations/users')
def view_all_conversations(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    return view_conversations(user.id)