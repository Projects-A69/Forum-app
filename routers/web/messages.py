from fastapi import APIRouter, Request, Form, Cookie, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from data.models import MessageCreate
from services.messages_service import create_messages, view_get_conversation, view_conversations
from services.users_service import find_by_username
from common.auth import get_user_or_raise_401
from datetime import date


templates = Jinja2Templates(directory="templates")

web_messages_router = APIRouter(prefix="/messages", tags=["Web Messages"])

@web_messages_router.get("/{receiver_id}")
def show_chat(request: Request, receiver_id: int, access_token: str | None = Cookie(default=None)):
    current_user = None
    try:
        current_user = get_user_or_raise_401(request.cookies.get("access_token"))
    except HTTPException:
        return templates.TemplateResponse("messages.html", {"request": request, "error": "You must login first."})
    conversation = view_conversations(current_user.id)
    messages = view_get_conversation(current_user.id, receiver_id)
    return templates.TemplateResponse("messages.html", {"request": request,
                                                        "messages": messages,
                                                        "conversation": conversation,
                                                        "receiver_id": receiver_id,
                                                        "user_id": current_user.id,
                                                        "current_user": current_user})

@web_messages_router.get("/")
def view_conversations_home(request: Request, access_token: str | None = Cookie(default=None)):
    current_user = None
    try:
        current_user = get_user_or_raise_401(request.cookies.get("access_token"))
    except HTTPException:
        return templates.TemplateResponse("messages.html", {"request": request, "error": "You must login first."})
    conversation = view_conversations(current_user.id)
    return templates.TemplateResponse("messages.html",{
                        'request':request,
                        "conversations": conversation,
                        'messages':[],
                        'receiver_id': None,
                        'user_id': current_user.id,
                        "current_user": current_user
                        })

@web_messages_router.post("/go")
def go_to_chat(receiver_id: int = Form()):
    return RedirectResponse(url = f"/messages/{receiver_id}", status_code = 302)

@web_messages_router.post("/create",)
def create_message_page(
        request: Request,
        sender_id: int = Form(),
        text: str = Form(),
        receiver_id: int = Form(),
        created_at: date = Form(),
        access_token: str | None = Cookie(default=None)):
    current_user = None
    try:
        current_user = get_user_or_raise_401(request.cookies.get("access_token"))
    except HTTPException:
        return templates.TemplateResponse("messages.html", {"request": request, "error": "You must login first."})

    messages_data = MessageCreate(
        sender_id=sender_id,
        receiver_id=receiver_id,
        text=text
    )
    create_messages(sender_id= current_user.id, receiver_id= messages_data.receiver_id, text=messages_data.text )

    return RedirectResponse(url=f"/messages/{receiver_id}", status_code=302)

@web_messages_router.post("/find")
def find_by_username_web(request: Request, username: str = Form() ,access_token: str | None = Cookie(default=None)):
    current_user = None
    try:
        current_user = get_user_or_raise_401(request.cookies.get("access_token"))
    except HTTPException:
        return templates.TemplateResponse("messages.html", {"request": request, "error": "You must login first."})

    if username.strip() == "":
        return templates.TemplateResponse("messages.html", {"request": request, "error": "You must enter a username!"})
    found = find_by_username(username)
    if not found:
        return templates.TemplateResponse("messages.html", {"request": request, "error": "User not found"}, status_code=400)
    conversations = view_conversations(current_user.id)
    messages = view_get_conversation(current_user.id, found.id)
    return templates.TemplateResponse("messages.html", {
        "request": request, "conversations": conversations, "messages": messages, "receiver_id": found.id, "user_id": current_user.id, "current_user": current_user})