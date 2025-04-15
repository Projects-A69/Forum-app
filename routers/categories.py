from fastapi import APIRouter

categories_router = APIRouter(prefix='/categories')


@categories_router.get("/")
def get_categories():
    # ToDo authentication will follow
    
    categories = services.get_all_categories()
    
    