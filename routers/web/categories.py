from fastapi import APIRouter, Request, Form, HTTPException, status, Cookie
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from common.auth import get_user_or_raise_401
from data.models import CategoryCreate
from services.categories_service import get_all_categories, create_category, get_by_id, lock_category
from services.users_service import is_authenticated, from_token

web_categories_router = APIRouter(prefix="/categories", tags=["Web - Categories"])
templates = Jinja2Templates(directory="templates")


@web_categories_router.get("/")
async def list_categories(
    request: Request,
    search: str = None,
    id: int = None,
    sort: str = "desc",
    access_token: str = Cookie(default=None)
):
    token = request.cookies.get("access_token")
    user = from_token(token)
    user_id = user.id if user else None

    categories = []
    error = None

    if id is not None:
        category = get_by_id(id, user_id=user_id)
        if category is None:
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error": f"Category with {id} does not exist."
            }, status_code=403)
        else:
            categories = [category]
    elif search:
        categories = get_all_categories(search=search, sort=sort)
    else:
        categories = get_all_categories(sort=sort)

    return templates.TemplateResponse("categories.html", {
        "request": request,
        "categories": categories,
        "search": search,
        "sort": sort,
        "error": error,
        "current_user": user
    })


@web_categories_router.get("/create")
async def create_category_form(request: Request):
    user = get_user_or_raise_401(request.cookies.get("access_token"))

    return templates.TemplateResponse("create_category.html", {
        "request": request,
        "current_user": user
    })


@web_categories_router.post("/create")
async def create_category_post(
    request: Request,
    name: str = Form(...),
    info: str = Form(""),
    is_private: str | None = Form(None)
):
    user = get_user_or_raise_401(request.cookies.get("access_token"))

    private_flag = bool(is_private) and user.is_admin

    try:
        category_create = CategoryCreate(
            name=name.strip(),
            info=info.strip(),
            is_private=private_flag,
            is_locked=False
        )
        category = create_category(category_create, token=request.cookies.get("access_token"))
    except ValueError as e:
        return templates.TemplateResponse("create_category.html", {
            "request": request,
            "error": str(e),
            "name": name,
            "info": info,
            "is_private": private_flag,
            "current_user": user
        })

    return RedirectResponse(url=f"/categories/{category.id}", status_code=status.HTTP_303_SEE_OTHER)


@web_categories_router.get("/{category_id}")
async def view_category(
    request: Request,
    category_id: int,
    search: str = None,
    sort: str = "date_created",
    order: str = "ASC"
):
    user = get_user_or_raise_401(request.cookies.get("access_token"))
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
    user = get_user_or_raise_401(request.cookies.get("access_token"))

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can lock/unlock categories.")

    lock_category(category_id, request.cookies.get("access_token"))

    return RedirectResponse(f"/categories/{category_id}", status_code=HTTP_302_FOUND)


@web_categories_router.get("/{category_id}/edit")
async def edit_category_form(request: Request, category_id: int):
    user = get_user_or_raise_401(request.cookies.get("access_token"))
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can edit categories.")

    category = get_by_id(
        id=category_id,
        search=None,
        sort_by="date_created",
        order="ASC",
        user_id=user.id
    )
    if category is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Category with ID {category_id} does not exist."
        }, status_code=403)

    return templates.TemplateResponse("edit_category.html", {
        "request": request,
        "category": category,
        "current_user": user
    })


@web_categories_router.post("/{category_id}/edit")
async def edit_category_post(
    request: Request,
    category_id: int,
    name: str = Form(...),
    info: str = Form(""),
    is_private: str = Form("off"),
):
    user = get_user_or_raise_401(request.cookies.get("access_token"))
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can edit categories.")

    is_private_flag = is_private.lower() == "on"

    from data.database import update_query
    try:
        update_query(
            '''
            UPDATE categories
            SET name = ?, info = ?, is_private = ?
            WHERE id = ?
            ''',
            (name.strip(), info.strip(), int(is_private_flag), category_id)
        )
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Error updating category: {str(e)}"
        }, status_code=500)

    return RedirectResponse(f"/categories/{category_id}", status_code=HTTP_302_FOUND)

@web_categories_router.post("/{category_id}/private-toggle")
async def toggle_private_category(request: Request, category_id: int):
    user = get_user_or_raise_401(request.cookies.get("access_token"))

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can toggle private status.")

    category = get_by_id(category_id, user_id=user.id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")

    new_private_status = not category.is_private

    from data.database import update_query
    try:
        update_query(
            '''
            UPDATE categories
            SET is_private = ?
            WHERE id = ?
            ''',
            (int(new_private_status), category_id)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update category privacy: {e}")

    return RedirectResponse(f"/categories/{category_id}", status_code=HTTP_302_FOUND)
