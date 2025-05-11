from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from data.models import RegisterData, LoginData, User
from services import users_service
import bcrypt

templates = Jinja2Templates(directory="templates")
web_users_router = APIRouter(prefix="/users", tags=["WEB USERS"])

@web_users_router.get("/register")
def show_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@web_users_router.post("/register")
def web_register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    telephone_number: str = Form(...),
    password: str = Form(...)):
    data = RegisterData(username=username,
        email=email,
        telephone_number=telephone_number,
        password=password)

    if users_service.find_by_username(data.username):
        return templates.TemplateResponse("register.html", {"request": request,
            "error": f"Username '{data.username}' is already taken. Please choose another one or login."})

    if users_service.find_by_email(data.email):
        return templates.TemplateResponse("register.html", {"request": request,
            "error": f"Email '{data.email}' is already registered. Please use a different email address or login."})

    if users_service.find_by_telephone(data.telephone_number):
        return templates.TemplateResponse("register.html", {"request": request,
            "error": f"Phone number '{data.telephone_number}' is already used. Please use a different number or login."})

    try:
        user = User(
            username=data.username,
            telephone_number=data.telephone_number,
            email=data.email,
            password=data.password
        )
        users_service.register_user(user)
        token = users_service.create_token(user)

        response = RedirectResponse(url="/users/dashboard", status_code=302)
        response.set_cookie(key="access_token", value=token, httponly=True, secure=True)
        response.set_cookie(key="flash_message", value=f"User '{data.username}' registered successfully.", max_age=5)
        return response
    except Exception as e:
        return templates.TemplateResponse("register.html", {"request": request,
            "error": f"An error occurred while registering the user: {str(e)}"})

@web_users_router.get("/login")
def show_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@web_users_router.post("/login")
def web_login(request: Request,
    username: str = Form(...),
    password: str = Form(...)):
    data = LoginData(username=username, password=password)

    user = users_service.find_by_username(data.username)
    if user and bcrypt.checkpw(data.password.encode(), user.password.encode()):
        token = users_service.create_token(user)
        response = RedirectResponse(url=f"/users/dashboard", status_code=302)
        response.set_cookie(key="access_token", value=token, httponly=True, secure=True)
        return response
    return templates.TemplateResponse("login.html", {"request": request,"error": "Invalid username or password."})

@web_users_router.get("/dashboard")
def show_dashboard(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/users/login", status_code=302)
    
    user = users_service.from_token(token)
    if not user:
        return RedirectResponse(url="/users/login", status_code=302)
    
    return templates.TemplateResponse("dashboard.html", {"request": request,"token": token,"current_user": user})
    
@web_users_router.get("/info")
def show_user_info(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/users/login", status_code=302)

    try:
        user = users_service.from_token(token)
        if not user:
            return RedirectResponse(url="/users/login", status_code=302)

        return templates.TemplateResponse("info.html", {
            "request": request,
            "user": {
                "id": user.id,
                "username": user.username,
                "telephone_number": user.telephone_number,
                "email": user.email,
                "is_admin": user.is_admin,
                "date_registration": user.date_registration
            }
        })
    except Exception as e:
        return templates.TemplateResponse("info.html", {
            "request": request,
            "error": f"An error occurred while fetching user info: {str(e)}"
        })