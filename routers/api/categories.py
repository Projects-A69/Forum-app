from fastapi import APIRouter,HTTPException, Header
from data.models import CategoryCreate
from services.categories_service import get_all, get_by_id, create_category, lock_category
from common.auth import get_user_or_raise_401



categories_router = APIRouter(prefix='/api/categories',tags=['Categories'])

@categories_router.get('/')
def get_categories(search: str | None = None):
    return get_all(search)


@categories_router.get('/{id}')
def get_category_by_id(id: int):
    category = get_by_id(id)

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    else:
        return category


@categories_router.post('/')
def create_categories_router(category: CategoryCreate,x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    return create_category(category,user.id)


@categories_router.put('/{id}/lock')
def lock_category_router(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required to lock a category")

    updated_category = lock_category(id)

    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return updated_category