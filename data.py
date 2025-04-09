from pydantic import BaseModel
from datetime import datetime

class Users(BaseModel): # Uasim
    pass

class Messages(BaseModel): # Dimatur
    pass

class Categories(BaseModel): # Ivan
    name_categories: int
    info_categories: str
    type_access_private: bool
    date_create_access: datetime = Field(default_factory = datetime.now)
    user_id_user: int

class Topics(BaseModel): # Uasim
    pass

class Replies(BaseModel): # Dimitur
    pass

class ReplyVotes(BaseModel): # Ivan
    id_replies: int
    vote_type: str
    created_at: datetime = Field(default_factory = datetime.now)
    replies_id: int
    user_id_user: int
