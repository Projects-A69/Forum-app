from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND

from services import categories_service
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
    token = get_token_from_request(request)
    user = get_current_user(request)
    user_id = user.id if user else None

    categories = categories_service.get_all_categories(search=search, sort=sort)
    return templates.TemplateResponse("categories.html", {
        "request": request,
        "categories": categories,
        "search": search,
        "sort": sort,
        "current_user": user
    })


@web_categories_router.get("/create")
async def create_category_form(request: Request):
    token = get_token_from_request(request)
    if not token or not is_authenticated(token):
        return RedirectResponse("/users/login", status_code=HTTP_302_FOUND)

    user = from_token(token)
    return templates.TemplateResponse("category_create.html", {
        "request": request,
        "current_user": user
    })


@web_categories_router.post("/create")
async def create_category_post(
    request: Request,
    name: str = Form(...),
    info: str = Form(""),
    is_private: bool = Form(False)
):
    token = get_token_from_request(request)
    user = from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    from data.models import CategoryCreate
    import datetime

    category = CategoryCreate(
        name=name,
        info=info,
        is_private=is_private,
        date_created=datetime.datetime.utcnow(),
        is_locked=False
    )

    categories_service.create_category(category, token)
    return RedirectResponse("/categories", status_code=HTTP_302_FOUND)


@web_categories_router.get("/{category_id}")
async def view_category(request: Request, category_id: int, search: str = None, sort: str = "date_created", order: str = "ASC"):
    token = get_token_from_request(request)
    user = get_current_user(request)
    user_id = user.id if user else None

    category = categories_service.get_by_id(
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
async def lock_category(request: Request, category_id: int):
    token = get_token_from_request(request)
    if not token or not is_authenticated(token):
        raise HTTPException(status_code=401, detail="Unauthorized")

    category = categories_service.lock_category(category_id, token)
    return RedirectResponse(f"/categories/{category_id}", status_code=HTTP_302_FOUND)
