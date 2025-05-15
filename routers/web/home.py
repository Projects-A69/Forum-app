from fastapi import APIRouter, Request,Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from services import users_service


templates = Jinja2Templates(directory="templates")

home_router = APIRouter()

@home_router.get("/")
def homepage(request: Request):
    token = request.cookies.get("access_token")
    current_user = None
    
    if token:
        user_obj = users_service.from_token(token)
        if user_obj:
            current_user = {"username": user_obj.username}
    
    return templates.TemplateResponse(
        "home.html", {"request": request, "current_user": current_user})
    
    
@home_router.get("/users/logout")
def logout(response: Response):
    response = RedirectResponse(url="/")
    response.delete_cookie(key="access_token")
    return response