from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.api.categories import categories_router
from routers.api.messages import messages_router
from routers.api.replies import replies_router
from routers.api.topics import topics_router
from routers.api.users import users_router
from routers.api.category_access import access_router

from routers.web.home import home_router
# from routers.web.topics import web_topics_router
from routers.web.users import web_users_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(categories_router)
app.include_router(messages_router)
app.include_router(replies_router)
app.include_router(topics_router)
app.include_router(users_router)
app.include_router(access_router)

app.include_router(home_router)
# app.include_router(web_topics_router)
app.include_router(web_users_router)





