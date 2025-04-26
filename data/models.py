from pydantic import BaseModel
from datetime import datetime


class Users(BaseModel):
    id: int | None = None
    username: str
    telephone_number: str
    email: str
    is_admin: bool | None = False
    password: str
    date_registration: datetime = None
    
    @classmethod
    def from_query_result(cls, id, username, telephone_number, email, is_admin=False, password='', date_registration=None):
        return cls(
            id=id,
            username=username,
            telephone_number=telephone_number,
            email=email,
            is_admin=is_admin if is_admin is not None else False,
            password=password,
            date_registration=date_registration or datetime.now())

class Categories(BaseModel):
    id: int
    name: str
    info: str
    is_private: bool = False
    date_created: datetime = None
    is_locked: bool = False
    
'''
class CategoryHasUsers(BaseModel):
    categories_id: int
    users_id: int
    acess_level: bool = False
'''

class Topics(BaseModel):
    id: int
    title: str
    text: str
    user_id: int
    category_id: int
    is_locked: int = 0
    date_create: datetime = datetime.now()
    best_reply_id: int = 0

    @classmethod
    def from_query_result(cls, id, title,text, user_id, category_id, is_locked=0, date_create=None, best_reply_id=0):
        return cls(
            id=id,
            title=title,
            text=text,
            user_id=user_id,
            category_id=category_id,
            is_locked=is_locked if is_locked is not None else 0,
            date_create=date_create or datetime.now(),
            best_reply_id=best_reply_id,)
        
        
class TopicCreate(BaseModel):
    title: str
    text:str
    category_id: int
    
class Replies(BaseModel):
    id:int
    text: str
    date_create: datetime = None
    date_update: datetime = None
    user_id: int
    topic_id: int
    

'''
class RepliesHasUsers(BaseModel):
    replies_id: int
    users_id: int
    vote_type: bool = False
 
reply_votes: list[RepliesHasUsers] = []
'''

class Messages(BaseModel):
    id: int
    sender_id : int
    text :str
    created_at: datetime = None
    receiver_id: int
    


