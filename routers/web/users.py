from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
web_users_router = APIRouter(prefix="/users")

@web_users_router.get("/")
def users_page(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})
