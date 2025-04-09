from pydantic import BaseModel
from datetime import datetime

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
    id: str
    sender: str
    reciever: str
    text_messages: str
    status: str
    created_at: datetime
    user_id: str

class Categories(BaseModel): # Ivan
    name_categories: int
    info_categories: str
    type_access_private: bool = False
    date_create_access: datetime = None
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
    author: str
    text_replies: str
    date_create: datetime
    date_update: datetime
    user_id: int
    topic_id: int

class ReplyVotes(BaseModel): # Ivan
    id_replies: int
    vote_type: str
    created_at: datetime = None
    replies_id: int
    user_id_user: int
