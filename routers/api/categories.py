from fastapi import APIRouter,HTTPException, Header, Query
from data.models import CategoryCreate
from services.categories_service import get_all, get_by_id, create_category, lock_category, view_categories
from common.auth import get_user_or_raise_401



categories_router = APIRouter(prefix='/api/categories',tags=['Categories'])

@categories_router.get('/')
def get_categories(search: str | None = None):
    return get_all(search)


@categories_router.get('/{id}')
def get_category_by_id(id: int, user_id: int):
    category = get_by_id(id, user_id)

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    if category == "no_write_access":
        raise HTTPException(status_code=403, detail="Access denied")

    return category

@categories_router.post('/')
def create_categories_router(category: CategoryCreate,x_token: str = Header()):
    get_user_or_raise_401(x_token)

    return create_category(category,x_token)

@categories_router.put('/{id}/lock')
def lock_category_router(id: int, x_token: str = Header()):
    return lock_category(id, x_token)

# @categories_router.put('/{id}/lock')
# def lock_category_router(id: int, x_token: str = Header()):
#     user = get_user_or_raise_401(x_token)

#     if not user.is_admin:
#         raise HTTPException(status_code=403, detail="Admin access required to lock a category")

#     updated_category = lock_category(id,x_token)

#     if updated_category is None:
#         raise HTTPException(status_code=404, detail="Category not found")

#     return updated_category

@categories_router.get('/')
def view_categories(
    search: str = Query(None, description="Search in category name or info"),
    sort: str = Query("desc", regex="^(asc|desc)$", description="Sort by date_created"),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0)
    ):

    return view_categories(search=search, sort=sort, offset=offset, limit=limit)