from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services.categories_service import get_all_categories, get_by_id, create_category, lock_category
from common.auth import get_user_or_raise_401

templates = Jinja2Templates(directory="templates")
web_categories_router = APIRouter(prefix="/categories", tags=["WEB CATEGORIES"])

@web_categories_router.get("/", response_class=HTMLResponse)
def show_categories(request: Request):
    current_user = None
    try:
        current_user = get_user_or_raise_401(request.cookies.get("access_token"))
    except HTTPException:
        pass

    categories = get_all_categories()
    return templates.TemplateResponse("categories.html", {
        "request": request,
        "categories": categories,
        "current_user": current_user
    })

@web_categories_router.get("/create", response_class=HTMLResponse)
def show_create_category_form(request: Request):
    try:
        user = get_user_or_raise_401(request.cookies.get("access_token"))
    except HTTPException:
        return RedirectResponse("/login", status_code=302)

    return templates.TemplateResponse("create_category.html", {
        "request": request,
        "user": user
    })

@web_categories_router.post("/", response_class=HTMLResponse)
def handle_create_category(request: Request, name: str = Form(...)):
    try:
        user = get_user_or_raise_401(request.cookies.get("access_token"))
    except HTTPException:
        return RedirectResponse("/login", status_code=302)

    result = create_category(name=name, user=user)

    if result == "name_taken":
        return templates.TemplateResponse("create_category.html", {
            "request": request,
            "error": "Category name already exists"
        }, status_code=400)

    return RedirectResponse("/categories", status_code=302)

@web_categories_router.get("/{id}", response_class=HTMLResponse)
def show_category_by_id(request: Request, id: int):
    category = get_by_id(id)
    if category is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Category not found"
        }, status_code=404)

    return templates.TemplateResponse("category.html", {
        "request": request,
        "category": category
    })

@web_categories_router.post("/{id}/lock", response_class=HTMLResponse)
def handle_lock_category(request: Request, id: int):
    try:
        user = get_user_or_raise_401(request.cookies.get("access_token"))
    except HTTPException:
        return RedirectResponse("/login", status_code=302)

    if not user.is_admin:
        return RedirectResponse(f"/categories/{id}", status_code=302)

    result = lock_category(id)
    if result == "category_not_found":
        return RedirectResponse("/categories", status_code=302)

    return RedirectResponse(f"/categories/{id}", status_code=302)
