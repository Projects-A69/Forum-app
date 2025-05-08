from fastapi import APIRouter, Header, HTTPException
from common.auth import get_user_or_raise_401
from services.category_access_service import grant_access, revoke_access, get_category_access
from data.models import CategoryAccessUpdate

access_router = APIRouter(prefix='/api/categories', tags=['Category Access'])

@access_router.put('/{category_id}/users/{user_id}/access')
def update_category_access(category_id: int, user_id: int, access: CategoryAccessUpdate, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required.")

    if access.access_level not in (0, 1):
        raise HTTPException(status_code=400, detail="Invalid access level. Use 0 for read, 1 for write.")

    grant_access(user_id, category_id, access.access_level)
    return {"message": f"Access level updated to {'read' if access.access_level == 0 else 'write'}."}

@access_router.delete('/{category_id}/users/{user_id}/access')
def delete_category_access(category_id: int, user_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required.")

    revoke_access(user_id, category_id)
    return {"message": "Access revoked."}

@access_router.get('/{category_id}/privileged-users')
def get_privileged_users(category_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required.")

    users = get_category_access(category_id)
    return [{
        "user_id": user["user_id"],
        "username": user["username"],
        "access_level": "read" if user["access_level"] == 0 else "write"
    } for user in users]
