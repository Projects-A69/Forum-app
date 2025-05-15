from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    id: int | None = None
    username: str
    telephone_number: str
    email: str
    is_admin: bool | None = False
    password: str
    date_registration: date = None
    
    @classmethod
    def from_query_result(cls, id, username, telephone_number, email, is_admin=False, password='', date_registration=None):
        return cls(
            id=id,
            username=username,
            telephone_number=telephone_number,
            email=email,
            is_admin=is_admin if is_admin is not None else False,
            password=password,
            date_registration=date_registration or date.today())
        
        
class RegisterData(BaseModel):
    username: str
    telephone_number: str
    email: str
    password: str


class LoginData(BaseModel):
    username: str
    password: str


class UserInfoResponse(BaseModel):
    id: int
    username: str
    telephone_number: str
    email: str
    is_admin: bool
    date_registration: date

    
class Reply(BaseModel):
    id:int
    text: str
    date_create: date = None
    date_update: date = None
    user_id: int
    topic_id: int

    @classmethod
    def from_query_result(cls, id, text, date_create, date_update, user_id, topic_id):
        return cls(
            id=id,
            text=text,
            date_create=date_create or date.today(),
            date_update=date_update or date.today(),
            user_id=user_id,
            topic_id=topic_id
        )


class ReplyCreate(BaseModel):
    text: str
    user_id: int
    topic_id: int

    
class Topic(BaseModel):
    id: int
    title: str
    text: str
    user_id: int
    category_id: int
    is_locked: int = 0
    date_create: date = None
    best_reply_id: int = 0
    replies: list[Reply] = []

    @classmethod
    def from_query_result(cls, id, title,text, user_id, category_id, is_locked=0, date_create=None, best_reply_id=0,replies = None):
        return cls(
            id=id,
            title=title,
            text=text,
            user_id=user_id,
            category_id=category_id,
            is_locked=is_locked if is_locked is not None else 0,
            date_create=date_create or date.today(),
            best_reply_id=best_reply_id,
            replies = replies or [])


class Category(BaseModel):
    id: int
    name: str
    info: str
    is_private: bool = False
    date_created: date = None
    is_locked: bool = False
    topics: list[Topic] = []

    @classmethod
    def from_query_result(cls, id, name ,info, is_private=0, date_created=None, is_locked=0, topics=None):
        return cls(
            id=id,
            name=name,
            info=info,
            is_private=is_private if is_private is not None else False,
            date_created=date_created or date.today(),
            is_locked=is_locked if is_locked is not None else False,
            topics=topics or [])

class CategoryCreate(BaseModel):
    name: str
    info:str
    date_created: date = None
    is_private: int = 0
    is_locked: int = 0

class TopicCreate(BaseModel):
    title: str
    text:str
    category_id: int

    
class Reply(BaseModel):
    id:int
    text: str
    date_create: date = None
    date_update: date = None
    user_id: int
    topic_id: int
    likes: int = 0
    dislikes: int = 0

    @classmethod
    def from_query_result(cls, id, text, date_create, date_update, user_id, topic_id):
        return cls(
            id=id,
            text=text,
            date_create=date_create or date.today(),
            date_update=date_update or date.today(),
            user_id=user_id,
            topic_id=topic_id)


class ReplyCreate(BaseModel):
    text: str
    user_id: int
    topic_id: int
    
class Topic(BaseModel):
    id: int
    title: str
    text: str
    user_id: int
    category_id: int
    is_locked: int = 0
    date_create: date = None
    best_reply_id: int = 0
    replies: list[Reply] = []

    @classmethod
    def from_query_result(cls, id, title,text, user_id, category_id, is_locked=0, date_create=None, best_reply_id=None,replies = None):
        return cls(
            id=id,
            title=title,
            text=text,
            user_id=user_id,
            category_id=category_id,
            is_locked=is_locked if is_locked is not None else 0,
            date_create=date_create or date.today(),
            best_reply_id=best_reply_id if best_reply_id is not None else 0,
            replies = replies or [])
        
        
class TopicCreate(BaseModel):
    title: str
    text:str
    category_id: int


class RepliesHasUsers(BaseModel):
    replies_id: int
    users_id: int
    vote_type: bool = False

reply_votes: list[RepliesHasUsers] = []


class Message(BaseModel):
    id: int
    sender_id : int
    text :str
    created_at: date = None
    receiver_id: int

    @classmethod
    def from_query_result(cls, id, sender_id,text, created_at, reciever_id):
        return cls(
            id=id,
            sender_id=sender_id,
            text=text,
            created_at=created_at or date.today(),
            receiver_id=reciever_id)


class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: int
    text:str

class CategoryAccess(BaseModel):
    categories_id: int
    users_id: int
    access_level: int

class CategoryAccessUpdate(BaseModel):
    access_level: int

class Category(BaseModel):
    id: int
    name: str
    info: str
    is_private: bool = False
    date_created: date = None
    is_locked: bool = False
    topics: list[Topic] = []

    @classmethod
    def from_query_result(cls, id, name ,info, is_private=0, date_created=None, is_locked=0, topics= None):
        return cls(
            id=id,
            name=name,
            info=info,
            is_private=is_private if is_private is not None else False,
            date_created=date_created or date.today(),
            is_locked=is_locked if is_locked is not None else False,
            topics = topics or [])
    

# from pydantic import BaseModel
# from datetime import date
# from typing import List


# class User(BaseModel):
#     id: int | None = None
#     username: str
#     telephone_number: str
#     email: str
#     is_admin: bool | None = False
#     password: str
#     date_registration: date = None
    
#     @classmethod
#     def from_query_result(cls, id, username, telephone_number, email, is_admin=False, password='', date_registration=None):
#         return cls(
#             id=id,
#             username=username,
#             telephone_number=telephone_number,
#             email=email,
#             is_admin=is_admin if is_admin is not None else False,
#             password=password,
#             date_registration=date_registration or date.today())
        
        
# class RegisterData(BaseModel):
#     username: str
#     telephone_number: str
#     email: str
#     password: str


# class LoginData(BaseModel):
#     username: str
#     password: str


# class UserInfoResponse(BaseModel):
#     id: int
#     username: str
#     telephone_number: str
#     email: str
#     is_admin: bool
#     date_registration: date


# class Reply(BaseModel):
#     id: int
#     text: str
#     date_create: date = None
#     date_update: date = None
#     user_id: int
#     topic_id: int

#     @classmethod
#     def from_query_result(cls, id, text, date_create, date_update, user_id, topic_id):
#         return cls(
#             id=id,
#             text=text,
#             date_create=date_create or date.today(),
#             date_update=date_update or date.today(),
#             user_id=user_id,
#             topic_id=topic_id
#         )


# class ReplyCreate(BaseModel):
#     text: str
#     user_id: int
#     topic_id: int


# class Topic(BaseModel):
#     id: int
#     title: str
#     text: str
#     user_id: int
#     category_id: int
#     is_locked: int = 0
#     date_create: date = None
#     best_reply_id: int = 0
#     replies: list[Reply] = []

#     @classmethod
#     def from_query_result(cls, id, title, text, user_id, category_id, is_locked=0, date_create=None, best_reply_id=0, replies=None):
#         return cls(
#             id=id,
#             title=title,
#             text=text,
#             user_id=user_id,
#             category_id=category_id,
#             is_locked=is_locked if is_locked is not None else 0,
#             date_create=date_create or date.today(),
#             best_reply_id=best_reply_id if best_reply_id is not None else 0,
#             replies=replies or [])


# class TopicCreate(BaseModel):
#     title: str
#     text: str
#     category_id: int


# class Category(BaseModel):
#     id: int
#     name: str
#     info: str
#     is_private: bool = False
#     date_created: date = None
#     is_locked: bool = False
#     topics: list[Topic] = []

#     @classmethod
#     def from_query_result(cls, id, name, info, is_private=0, date_created=None, is_locked=0, topics=None):
#         return cls(
#             id=id,
#             name=name,
#             info=info,
#             is_private=is_private if is_private is not None else False,
#             date_created=date_created or date.today(),
#             is_locked=is_locked if is_locked is not None else False,
#             topics=topics or [])


# class CategoryCreate(BaseModel):
#     name: str
#     info: str
#     date_created: date = None
#     is_private: int = 0
#     is_locked: int = 0


# class CategoryAccess(BaseModel):
#     categories_id: int
#     users_id: int
#     access_level: int


# class CategoryAccessUpdate(BaseModel):
#     access_level: int


# class Message(BaseModel):
#     id: int
#     sender_id: int
#     text: str
#     created_at: date = None
#     receiver_id: int

#     @classmethod
#     def from_query_result(cls, id, sender_id, text, created_at, reciever_id):
#         return cls(
#             id=id,
#             sender_id=sender_id,
#             text=text,
#             created_at=created_at or date.today(),
#             receiver_id=reciever_id)


# class MessageCreate(BaseModel):
#     sender_id: int
#     receiver_id: int
#     text: str


# class RepliesHasUsers(BaseModel):
#     replies_id: int
#     users_id: int
#     vote_type: bool = False


# reply_votes: list[RepliesHasUsers] = []

