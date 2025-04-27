from data.database import read_query, insert_query
from data.models import Users
from datetime import datetime
import bcrypt

_SEPARATOR = ';'

def find_by_username(username: str) -> Users | None:
    data = read_query(
        '''SELECT id, username, telephone_number, email, is_admin, password, date_registration 
           FROM users WHERE username = ?''',
        (username,))
    if not data:
        return None

    return Users.from_query_result(*data[0])

def find_by_email(email: str) -> Users | None:
    data = read_query(
        '''SELECT id, username, telephone_number, email, is_admin, password, date_registration 
           FROM users WHERE email = ?''',
        (email,))
    if not data:
        return None

    return Users.from_query_result(*data[0])


def find_by_telephone(telephone_number: str) -> Users | None:
    data = read_query(
        '''SELECT id, username, telephone_number, email, is_admin, password, date_registration 
           FROM users WHERE telephone_number = ?''',
        (telephone_number,))
    if not data:
        return None

    return Users.from_query_result(*data[0])


def create_token(user: Users) -> str:
    return f'{user.id}{_SEPARATOR}{user.username}'


def is_authenticated(token: str) -> bool:
    try:
        user_id, username = token.split(_SEPARATOR)
        user = find_by_username(username)
        return user is not None and str(user.id) == user_id
    except Exception:
        return False


def from_token(token: str) -> Users | None:
    try:
        _, username = token.split(_SEPARATOR)
        return find_by_username(username)
    except Exception:
        return None


def register_user(user_data: Users) -> Users:
    hashed_password = bcrypt.hashpw(user_data.password.encode(), bcrypt.gensalt())
    user_id = insert_query(
        '''INSERT INTO users (username, telephone_number, email, password)
           VALUES (?, ?, ?, ?)''',
            (user_data.username,
            user_data.telephone_number,
            user_data.email,
            hashed_password,))
    user_data.id = user_id
    return user_data


