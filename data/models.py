from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int = None
    first_name: str
    last_name : str
    telephone_number: str
    email: str
    is_admin: bool = False
    password: str
    date_registration: datetime = None

users:list[User] = []

class Messages(BaseModel):
    id: int     #change
    sender: str
    reciever: str
    text_messages: str
    status: str
    created_at: datetime = None
    user_id: int
    
messages: list[Messages] = []


class Categories(BaseModel):
    id_categories: int #change
    categories_name:str         #change
    info_categories: str
    type_access_private: bool = False
    date_create_access: datetime = None
    user_id_user: int
    
categories: list[Categories] = []


class Topics(BaseModel):
    id: int
    title: str
    user_id: int
    category_id: int
    is_locked: bool = None
    created_at: datetime
    best_reply_id: int
    
topics: list[Topics] = []


class Replies(BaseModel):
    replies_id:int
   # author: str          #change
    text_replies: str
    date_create: datetime = None
    date_update: datetime = None
    user_id: int
    topic_id: int
    
replies: list[Replies] = []


class ReplyVotes(BaseModel):
    id_replies: int
    vote_type: str
    created_at: datetime = None
    replies_id: int
    user_id_user: int
    
reply_votes: list[ReplyVotes] = []


