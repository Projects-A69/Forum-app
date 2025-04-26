from data.models import Messages, MessagesCreate
from services.messages_service import create_message
from fastapi import APIRouter
from pydantic import BaseModel
from routers.categories import categories_router


messages_router = APIRouter(prefix='/messages')

@messages_router.post('/create',)
def create(message: MessagesCreate):
    return create_message(message.receiver_id, message.text)
