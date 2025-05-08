from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

home_router = APIRouter()

@home_router.get("/")
def homepage(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
