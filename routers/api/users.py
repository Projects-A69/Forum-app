from fastapi import APIRouter, Header,Response
from common.auth import get_user_or_raise_401
from common.responses import BadRequest,Unauthorized,NotFound
from data.models import LoginData, RegisterData,User
from services import users_service
import bcrypt

users_router = APIRouter(prefix='/api/users',tags=['USERS'])


@users_router.post('/login')
def login(data: LoginData):
    user = users_service.find_by_username(data.username)

    if user and bcrypt.checkpw(data.password.encode(), user.password.encode()):
        token = users_service.create_token(user)
        return {'token': token}
    else:
        return BadRequest('Invalid username or password')

@users_router.get('/info')
def user_info(x_token: str = Header()):
    user =  get_user_or_raise_401(x_token)
    return {
        "id": user.id,
        "username": user.username,
        "telephone_number": user.telephone_number,
        "email": user.email,
        "is_admin": user.is_admin,
        "date_registration": user.date_registration
    }


@users_router.post('/register')
def register(data: RegisterData):
    if users_service.find_by_username(data.username):
        return BadRequest(f"Username '{data.username}' is already taken. Please choose another one or login.")

    if users_service.find_by_email(data.email):
        return BadRequest(f"Email '{data.email}' is already registered. Please use a different email address or login.")

    if users_service.find_by_telephone(data.telephone_number):
        return BadRequest(f"Phone number '{data.telephone_number}' is already used. Please use a different number or login.")

    user_data = User(
        username=data.username,
        telephone_number=data.telephone_number,
        email=data.email,
        password=data.password)

    user = users_service.register_user(user_data)
    return Response(status_code=200, content = f"User '{user.username}' registered successfully")

@users_router.put("/{user_id}/admin")
def promote_to_admin(user_id: int, x_token: str = Header()):
    user = users_service.from_token(x_token)
    if not user:
        return Unauthorized("Invalid or missing token.")

    result = users_service.make_user_admin(user, user_id)

    if result is False:
        return BadRequest("Only admins can promote users to admin.")
    elif result is None:
        return NotFound(f"User with ID {user_id} not found.")

    return Response(status_code=200, content=f"User with ID {user_id} is now an admin.")


