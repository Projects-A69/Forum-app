from data.database import read_query, insert_query,update_query
from data.models import User
from datetime import datetime,timedelta,timezone
from jose import jwt
import bcrypt

SECRET_KEY = "123"
ALGORITHM = "HS256"
TOKEN_EXPIRATION_TIME = 60

def find_by_username(username: str) -> User | None:
    data = read_query('''SELECT id, username, telephone_number, email, is_admin, password, date_registration 
           FROM users WHERE username = ?''',(username,))
    if not data:
        return None

    return User.from_query_result(*data[0])


def create_token(user: User) -> str:
    payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.now(timezone.utc)+ timedelta(minutes = TOKEN_EXPIRATION_TIME)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def is_authenticated(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        user = find_by_username(username)
        return user is not None and str(user.id) == str(payload.get("user_id"))
    except Exception:
        return False

def from_token(token: str) -> User | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        return find_by_username(username)
    except Exception:
        return None
    
def register_user(user_data: User) -> User:
    hashed_password = bcrypt.hashpw(user_data.password.encode(), bcrypt.gensalt())
    user_id = insert_query('''INSERT INTO users (username, telephone_number, email, password)
           VALUES (?, ?, ?, ?)''',(user_data.username,user_data.telephone_number,user_data.email,hashed_password,))
    user_data.id = user_id
    return user_data

def make_user_admin(requesting_user: User, target_user_id: int) -> bool | None:
    if not requesting_user.is_admin:
        return False

    user = read_query("SELECT id FROM users WHERE id = ?", (target_user_id,))
    if not user:
        return None

    update_query("UPDATE users SET is_admin = 1 WHERE id = ?", (target_user_id,))
    return True



def find_by_email(email: str) -> User | None:
    data = read_query(
        '''SELECT id, username, telephone_number, email, is_admin, password, date_registration 
           FROM users WHERE email = ?''',
        (email,))
    if not data:
        return None

    return User.from_query_result(*data[0])


def find_by_telephone(telephone_number: str) -> User | None:
    data = read_query(
        '''SELECT id, username, telephone_number, email, is_admin, password, date_registration 
           FROM users WHERE telephone_number = ?''',
        (telephone_number,))
    if not data:
        return None

    return User.from_query_result(*data[0])

def get_all_users() -> list[User]:
    data = read_query(
        '''SELECT id, username, telephone_number, email, is_admin, password, date_registration FROM users'''
    )
    return [User.from_query_result(*row) for row in data]