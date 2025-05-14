from fastapi import APIRouter,HTTPException, Header, Query
from data.models import CategoryCreate, Category
from services.categories_service import get_by_id, create_category, lock_category, get_all_categories
from common.auth import get_user_or_raise_401



categories_router = APIRouter(prefix='/api/categories',tags=['Categories'])

@categories_router.get('/')
def view_categories_router(
    search: str | None = None,
    sort: str = Query("desc", regex="^(asc|desc)$", description="Sort by date_created"),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0)
):
    return get_all_categories(search=search, sort=sort, offset=offset, limit=limit)


@categories_router.get("/categories/{id}", response_model=Category)
def view_category_router(
    id: int,
    search: str = Query(None),
    sort_by: str = Query("date_created"),
    order: str = Query("ASC"),
    user_id: int = Query(None)
):
    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID must be provided for access control.")

    category = get_by_id(id=id, search=search, sort_by=sort_by, order=order, user_id=user_id)

    if category == "no_write_access":
        raise HTTPException(status_code=403, detail="You do not have permission to view this category")
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category

@categories_router.post('/')
def create_categories_router(category: CategoryCreate,x_token: str = Header()):
    get_user_or_raise_401(x_token)

    return create_category(category,x_token)

@categories_router.put('/{id}/lock')
def lock_category_router(id: int, x_token: str = Header()):
    return lock_category(id, x_token)
