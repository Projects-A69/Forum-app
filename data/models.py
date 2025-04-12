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
    id: int     #change
    sender_id: str
    text: str
    status: str
    created_at: datetime = None
    conversations_id: int
    
messages: list[Messages] = []

class Conversations(BaseModel):
    id: int
    name: str

class Conversations_has_user(BaseModel):
    conversations_id: int
    users_id: int

class Categories(BaseModel):
    id: int
    name: str
    info: str
    is_private: bool = False
    date_create_access: datetime = None
    user_id_user: int
    
categories: list[Categories] = []

class Category_acess(BaseModel):
    id: int
    user_id: int
    category_id: int
    acess_level: str

class Topics(BaseModel):
    id: int
    title: str
    user_id: int
    category_id: int
    is_locked: bool = None
    info_views: int
    date_create: datetime = None
    
topics: list[Topics] = []


class Replies(BaseModel):
    replies_id:int
    author: str
    text: str
    date_create: datetime = None
    date_update: datetime = None
    user_id: int
    topic_id: int
    is_best_reply: bool = None
    
replies: list[Replies] = []


class RepliesVotes(BaseModel):
    id: int
    vote_type: str
    created_at: datetime = None
    reply_id: int
    user_id: int
    
reply_votes: list[RepliesVotes] = []

class Messages(BaseModel):
    id: int
    vote_type: str
    created_at: datetime = None
    reply_id: int
    user_id: int

