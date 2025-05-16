from fastapi import APIRouter, Request, Form, HTTPException, Cookie
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from data.models import TopicCreate
from services.topics_service import get_all,get_by_id,create_topic,lock_topic,choose_best_reply,get_topic_with_replies
from common.auth import get_user_or_raise_401
from data.database import insert_query
from services.replies_service import vote_replies, create_replies

templates = Jinja2Templates(directory="templates")
web_topics_router = APIRouter(prefix="/topics", tags=["WEB TOPICS"])

@web_topics_router.get("/", response_class=HTMLResponse)
def show_topics(request: Request,id: int | None = None, search: str | None = None, sort: str | None = None):
    current_user = None
    try:
        current_user = get_user_or_raise_401(request.cookies.get("access_token"))
    except HTTPException:
        pass

    if id is not None:
        topic = get_by_id(id)
        if topic is None:
            return templates.TemplateResponse("error.html", {"request": request,
                "error": "Topic not found"
            }, status_code=404)
        return templates.TemplateResponse("topic.html", {
            "request": request,
            "topic": topic})
    if sort not in (None, "asc", "desc"):
        return templates.TemplateResponse("error.html", {"request": request,
            "error": "Invalid sort value. Use 'asc' or 'desc'."}, status_code=400)

    topics = get_all(search, sort)

    return templates.TemplateResponse("topics.html", {"request": request,
        "topics": topics,
        "search": search,
        "sort": sort,
        "current_user": current_user})

@web_topics_router.get("/create", response_class=HTMLResponse)
def show_create_topic_form(request: Request):
    try:
        current_user = get_user_or_raise_401(request.cookies.get("access_token"))
    except HTTPException:
        return RedirectResponse("/login", status_code=302)

    return templates.TemplateResponse("create_topic.html", {"request": request,
        "current_user": current_user})

@web_topics_router.get("/{id}", response_class=HTMLResponse)
def show_topic(request: Request, id: int):
    current_user = None
    try:
        current_user = get_user_or_raise_401(request.cookies.get("access_token"))
    except HTTPException:
        pass

    topic = get_by_id(id)
    
    if topic is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Topic not found"
        }, status_code=404)
    
    topic_with_replies = get_topic_with_replies(id)

    return templates.TemplateResponse("topic.html", {
        "request": request,
        "topic": topic_with_replies,
        "current_user": current_user})

@web_topics_router.post("/", response_class=HTMLResponse)
def handle_create_topic(
    request: Request,
    title: str = Form(...),
    text: str = Form(...),
    category_id: int = Form(...)):
    try:
        user = get_user_or_raise_401(request.cookies.get("access_token"))
    except HTTPException:
        return RedirectResponse("/login", status_code=302)

    topic_data = TopicCreate(
        title=title,
        text=text,
        category_id=category_id)

    result = create_topic(topic_data, user.id)

    if result == "category_not_found":
        return templates.TemplateResponse("create_topic.html", {
            "request": request,
            "error": "Category not found"
        }, status_code=404)
    if result == "category_locked":
        return templates.TemplateResponse("create_topic.html", {
            "request": request,
            "error": "This category is locked and cannot accept new topics"
        }, status_code=403)
    if result == "no_write_access":
        return templates.TemplateResponse("create_topic.html", {
            "request": request,
            "error": "You don't have write access to this category"
        }, status_code=403)
    if result == "category_private":
        return templates.TemplateResponse("create_topic.html", {
            "request": request,
            "error": "This category is private and you don't have access"
        }, status_code=403)

    return RedirectResponse(f"/topics/{result.id}", status_code=302)




@web_topics_router.post("/{id}/lock", response_class=HTMLResponse)
def handle_lock_topic(request: Request, id: int):
    try:
        user = get_user_or_raise_401(request.cookies.get("access_token"))
    except HTTPException:
        return RedirectResponse("/login", status_code=302)

    if not user.is_admin:
        return RedirectResponse(f"/topics/{id}", status_code=302)

    current_topic = get_by_id(id)
    if current_topic is None:
        return RedirectResponse("/topics", status_code=302)

    if current_topic.is_locked:
        insert_query('UPDATE topics SET is_locked = 0 WHERE id = ?', (id,))
    else:
        lock_topic(id)

    return RedirectResponse(f"/topics/{id}", status_code=302)


@web_topics_router.post("/{topic_id}/best-reply/{reply_id}", response_class=HTMLResponse)
def handle_best_reply(request: Request, topic_id: int, reply_id: int):
    try:
        user = get_user_or_raise_401(request.cookies.get("access_token"))
    except HTTPException:
        return RedirectResponse("/login", status_code=302)

    topic = get_by_id(topic_id)
    if topic is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Topic not found"
        }, status_code=404)

    if user.id != topic.user_id:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Only the topic author can choose the best reply"
        }, status_code=403)

    result = choose_best_reply(topic_id, reply_id, user.id)

    if result == "topic_not_found":
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Topic not found"
        }, status_code=404)
    if result == "not_author":
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Only the topic author can choose the best reply."
        }, status_code=403)
    if result == "reply_not_found":
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Reply not found for this topic."
        }, status_code=404)

    return RedirectResponse(f"/topics/{topic_id}", status_code=302)

@web_topics_router.post("/{topic_id}/replies")
def handle_replies(
    request: Request,
    topic_id: int,
    text: str = Form(),
    access_token: str | None = Cookie(default=None)
):
    try:
        user = get_user_or_raise_401(access_token)
    except HTTPException:
        return RedirectResponse("/login", status_code=302)
    if text.strip() == "":
        topic = get_by_id(topic_id)
        return templates.TemplateResponse("topic.html", {"request": request, "topic": topic, "error": "Input your reply"})
    create_replies(text, user.id, topic_id)
    return RedirectResponse(f"/topics/{topic_id}", status_code=302)

@web_topics_router.post("/{topic_id}/replies/{reply_id}")
def handle_votes(
    request: Request,
    topic_id: int,
    reply_id: int,
    vote_type: int = Form(...),
    access_token: str | None = Cookie(default=None)
):
    try:
        user = get_user_or_raise_401(access_token)
    except HTTPException:
        return RedirectResponse("/login", status_code=302)

    result = vote_replies(users_id=user.id, replies_id=reply_id, vote_type=vote_type)

    return RedirectResponse(f"/topics/{topic_id}", status_code=302)
