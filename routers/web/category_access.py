from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from services import users_service, categories_service, category_access_service

templates = Jinja2Templates(directory="templates")
admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.get("", response_class=HTMLResponse)
def admin_panel(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/users/login", status_code=302)
    
    user = users_service.from_token(token)
    if not user or not user.is_admin:
        return RedirectResponse(url="/users/dashboard", status_code=302)
    
    categories = categories_service.get_private_categories()
    return templates.TemplateResponse("admin_panel.html", {"request": request,
        "categories": categories,
        "current_user": user})

@admin_router.get("/category/{category_id}", response_class=HTMLResponse)
def manage_category_access(request: Request, category_id: int):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/users/login", status_code=302)
    
    user = users_service.from_token(token)
    if not user or not user.is_admin:
        return RedirectResponse(url="/users/dashboard", status_code=302)
    
    category = categories_service.get_by_id(category_id,user.id)
    if not category or not category.is_private:
        return RedirectResponse(url="/admin", status_code=302)
    
    users_with_access = category_access_service.get_category_access(category_id)
    all_users = users_service.get_all_users()
    
    return templates.TemplateResponse("manage_access.html", {"request": request,
        "category": category,
        "users_with_access": users_with_access,
        "all_users": all_users,
        "current_user": user})

@admin_router.post("/category/{category_id}/grant")
def grant_access(request: Request, category_id: int, user_id: int = Form(...), 
                access_level: int = Form(...)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/users/login", status_code=302)
    
    user = users_service.from_token(token)
    if not user or not user.is_admin:
        return RedirectResponse(url="/users/dashboard", status_code=302)
    
    category = categories_service.get_by_id(category_id, user.id)
    if not category or not category.is_private:
        return RedirectResponse(url="/admin", status_code=302)
    
    category_access_service.grant_access(user_id, category_id, access_level)
    return RedirectResponse(url=f"/admin/category/{category_id}", status_code=303)

@admin_router.post("/category/{category_id}/revoke/{user_id}")
def revoke_access(request: Request, category_id: int, user_id: int):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/users/login", status_code=302)
    
    user = users_service.from_token(token)
    if not user or not user.is_admin:
        return RedirectResponse(url="/users/dashboard", status_code=302)
    
    category_access_service.revoke_access(user_id, category_id)
    return RedirectResponse(url=f"/admin/category/{category_id}", status_code=303)
