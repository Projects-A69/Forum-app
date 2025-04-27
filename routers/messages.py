from data.models import Messages, MessagesCreate
from services.messages_service import create_message, view_conversation
from fastapi import APIRouter
from pydantic import BaseModel
from routers.categories import categories_router


messages_router = APIRouter(prefix='/messages')

@messages_router.post('/create',)
def create(message: MessagesCreate):
    return create_message(message.sender_id, message.receiver_id, message.text)

@messages_router.get('/conversation')
def view(sender_id: int, receiver_id: int):
    return view_conversation(sender_id, receiver_id)