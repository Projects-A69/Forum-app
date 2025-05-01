from data.models import Message, MessageCreate
from services.messages_service import create_message, view_conversation, view_conversations
from fastapi import APIRouter
from pydantic import BaseModel
from routers.categories import categories_router


messages_router = APIRouter(prefix='/api/messages')

@messages_router.post('/create',)
def create(message: MessageCreate):
    return create_message(message.sender_id, message.receiver_id, message.text)

@messages_router.get('/users/user_id')
def view(sender_id: int, receiver_id: int):
    return view_conversation(sender_id, receiver_id)

@messages_router.get('/conversations/users')
def view_all_conversations(id: int):
    return view_conversations(id)