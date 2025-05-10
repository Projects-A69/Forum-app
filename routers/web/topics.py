from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from data.models import TopicCreate
from services.topics_service import get_all, get_by_id, create_topic, lock_topic, choose_best_reply
from common.auth import get_user_or_raise_401

templates = Jinja2Templates(directory="templates")
web_topics_router = APIRouter(prefix="/topics", tags=["WEB TOPICS"])

@web_topics_router.get("/")
def show_topics_page(request: Request, search: str = None, sort: str = None):
    if sort not in (None, 'asc', 'desc'):
        return RedirectResponse(url="/error?message=Invalid+sort+value.+Use+'asc'+or+'desc'", status_code=302)
    
    topics = get_all(search, sort)
    return templates.TemplateResponse("topics.html", {
        "request": request,
        "topics": topics,
        "search": search,
        "sort": sort})
@web_topics_router.get("/search")
def search_topic_by_id_web(request: Request, id: int):
    topic = get_by_id(id)
    if topic is None:
        return RedirectResponse(url="/error?message=Topic+not+found", status_code=302)

    return RedirectResponse(url=f"/topics/{id}", status_code=302)


@web_topics_router.get("/create")
def show_create_topic_page(request: Request):
    return templates.TemplateResponse("create_topic.html", {"request": request})

@web_topics_router.post("/create")
def create_topic_web(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    category_id: int = Form(...),
    x_token: str = Form(...)):
    user = get_user_or_raise_401(x_token)
    topic_data = TopicCreate(
        title=title,
        content=content,
        category_id=category_id)
    result = create_topic(topic_data, user.id)
    
    if result == "category_not_found":
        return RedirectResponse(url="/error?message=Category+not+found", status_code=302)
    if result == "category_locked":
        return RedirectResponse(url="/error?message=Category+is+locked", status_code=302)
        
    return RedirectResponse(url=f"/topics/{result.id}", status_code=302)

@web_topics_router.post("/{id}/lock")
def lock_topic_web(
    request: Request,
    id: int,
    x_token: str = Form(...)):
    user = get_user_or_raise_401(x_token)
    if not user.is_admin:
        return RedirectResponse(url="/error?message=Admin+access+required", status_code=302)
    
    updated_topic = lock_topic(id)
    if updated_topic is None:
        return RedirectResponse(url="/error?message=Topic+not+found", status_code=302)
        
    return RedirectResponse(url=f"/topics/{id}", status_code=302)

@web_topics_router.post("/{topic_id}/best-reply/{reply_id}")
def choose_best_reply_web(
    request: Request,
    topic_id: int,
    reply_id: int,
    x_token: str = Form(...)):
    user = get_user_or_raise_401(x_token)
    result = choose_best_reply(topic_id, reply_id, user.id)
    
    if result == "topic_not_found":
        return RedirectResponse(url="/error?message=Topic+not+found", status_code=302)
    if result == "not_author":
        return RedirectResponse(url="/error?message=Not+the+topic+author", status_code=302)
    if result == "reply_not_found":
        return RedirectResponse(url="/error?message=Reply+not+found", status_code=302)
        
    return RedirectResponse(url=f"/topics/{topic_id}", status_code=302)

@web_topics_router.get("/{id}")
def show_topic_page(request: Request, id: int):
    topic = get_by_id(id)
    if topic is None:
        return RedirectResponse(url="/error?message=Topic+not+found", status_code=302)
    
    return templates.TemplateResponse("topic_detail.html", {
        "request": request,
        "topic": topic})
    
