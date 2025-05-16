from datetime import datetime
from fastapi import APIRouter, Request, Form, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from common.auth import get_user_or_raise_401
from data.models import CategoryCreate
from services.categories_service import get_all_categories, create_category, get_by_id, lock_category
from services.users_service import is_authenticated, from_token

web_categories_router = APIRouter(prefix="/categories", tags=["Web - Categories"])
templates = Jinja2Templates(directory="templates")


def get_token_from_request(request: Request) -> str | None:
    return request.cookies.get("access_token")


def get_current_user(request: Request):
    token = get_token_from_request(request)
    if token and is_authenticated(token):
        return from_token(token)
    return None


@web_categories_router.get("/")
async def list_categories(
    request: Request,
    search: str = None,
    sort: str = "desc",
):
    user = get_current_user(request)
    user_id = user.id if user else None

    categories = []

    if search:
        if search.isdigit():
            category = get_by_id(
                category_id=int(search),
                user_id=user_id
            )
            if category and category != "no_write_access":
                categories = [category]
        else:
            categories = get_all_categories(search=search, sort=sort)
    else:
        categories = get_all_categories(sort=sort)

    return templates.TemplateResponse("categories.html", {
        "request": request,
        "categories": categories,
        "search": search,
        "sort": sort,
        "current_user": user
    })

@web_categories_router.get("/create")
async def create_category_form(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/users/login", status_code=HTTP_302_FOUND)

    return templates.TemplateResponse("category_create.html", {
        "request": request,
        "current_user": user
    })


@web_categories_router.post("/create")
async def create_category_post(
    request: Request,
    name: str = Form(...),
    info: str = Form(""),
    is_private: str | None = Form(None),
    token: str = Depends(get_user_or_raise_401)
):
    user = from_token(token)

    private_flag = bool(is_private) and user.is_admin

    try:
        category_create = CategoryCreate(
            name=name.strip(),
            info=info.strip(),
            is_private=private_flag,
            date_created=datetime.utcnow(),
            is_locked=False
        )
        category = create_category(category_create, token)
    except ValueError as e:
        context = {
            "request": request,
            "error": str(e),
            "name": name,
            "info": info,
            "is_private": private_flag,
            "current_user": user
        }
        return templates.TemplateResponse("category_create.html", context)

    return RedirectResponse(url=f"/categories/{category.id}", status_code=status.HTTP_303_SEE_OTHER)


@web_categories_router.get("/{category_id}")
async def view_category(request: Request, category_id: int, search: str = None, sort: str = "date_created", order: str = "ASC"):
    user = get_current_user(request)
    user_id = user.id if user else None

    category = get_by_id(
        category_id,
        search=search,
        sort_by=sort,
        order=order,
        user_id=user_id
    )

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    if category == "no_write_access":
        raise HTTPException(status_code=403, detail="You do not have access to this category.")

    return templates.TemplateResponse("category_detail.html", {
        "request": request,
        "category": category,
        "current_user": user
    })


@web_categories_router.post("/{category_id}/lock")
async def lock_category_post(request: Request, category_id: int):
    token = get_token_from_request(request)
    if not token or not is_authenticated(token):
        raise HTTPException(status_code=401, detail="Unauthorized")

    lock_category(category_id, token)
    return RedirectResponse(f"/categories/{category_id}", status_code=HTTP_302_FOUND)
