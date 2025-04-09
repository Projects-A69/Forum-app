from pydantic import BaseModel
from datetime import datetime

class Users(BaseModel): # Uasim
    pass
class Users(BaseModel):
    id: int | None
    first_name: str
    last_name : str
    telephone_number: int
    email: str
    is_admin: bool = False
    password: str
    date_registration: datetime = None

class Messages(BaseModel): # Dimatur
    pass

class Categories(BaseModel): # Ivan
    name_categories: int
    info_categories: str
    type_access_private: bool
    date_create_access: datetime = Field(default_factory = datetime.now)
    user_id_user: int

class Topics(BaseModel):
    id: int
    title: str
    user_id: int
    category_id: int
    is_locked: bool = None
    created_at: datetime
    best_reply_id: int

class Replies(BaseModel): # Dimitur
    pass

class ReplyVotes(BaseModel): # Ivan
    id_replies: int
    vote_type: str
    created_at: datetime = Field(default_factory = datetime.now)
    replies_id: int
    user_id_user: int
