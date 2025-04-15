from data.models import Messages
from fastapi import APIRouter
from pydantic import BaseModel
from routers.categories import categories_router


messages_router = APIRouter(prefix='/messages')
