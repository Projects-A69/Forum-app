from pydantic import BaseModel
from datetime import datetime

class Users(BaseModel):
    id: int = None
    first_name: str
    last_name : str
    telephone_number: str
    email: str
    is_admin: bool = False
    password: str
    date_registration: datetime = None

users:list[Users] = []


class Messages(BaseModel):
    id: int
    sender_id: int
    reciever_id: int
    text: str
    status: str
    created_at: datetime = None
    
messages: list[Messages] = []


class Categories(BaseModel):
    id: int
    name: str
    info: str
    is_private: bool = False
    date_create_access: datetime = None
    
categories: list[Categories] = []


class CategoryHasUsers(BaseModel):
    categories_id: int
    users_id: int
    acess_level: bool = False


class Topics(BaseModel):
    id: int
    title: str
    user_id: int
    category_id: int
    is_locked: bool = None
    date_create: datetime = None
    best_reply_id: int
    
topics: list[Topics] = []


class Replies(BaseModel):
    replies_id:int
    text: str
    date_create: datetime = None
    date_update: datetime = None
    user_id: int
    topic_id: int
    
replies: list[Replies] = []


class RepliesHasUsers(BaseModel):
    replies_id: int
    users_id: int
    vote_type: bool = False     #check
 
reply_votes: list[RepliesHasUsers] = []    #check


class Messages(BaseModel):
    id: int
    vote_type: str
    created_at: datetime = None
    reply_id: int
    user_id: int

