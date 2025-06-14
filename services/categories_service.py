from fastapi import HTTPException
from data.database import read_query, insert_query, update_query
from data.models import Category, CategoryCreate
from common.auth import get_user_or_raise_401
from data.models import Topic
from services.category_access_service import has_access

def get_all_categories(search: str = None, sort: str = "desc", offset: int = 0, limit: int = 10):
    query = '''
        SELECT id, name, info, is_private, date_created, is_locked 
        FROM categories WHERE 1=1
    '''
    params = []

    if search:
        query += ' AND (name LIKE ? OR info LIKE ?)'
        like_param = f'%{search}%'
        params.extend([like_param, like_param])

    query += f' ORDER BY date_created {sort.upper()} LIMIT ? OFFSET ?'
    params.extend([limit, offset])

    data = read_query(query, tuple(params))
    return [Category.from_query_result(*row) for row in data]


def get_by_id(id: int, search: str = None, sort_by: str = "date_created", order: str = "ASC", user_id: int = None):
    allowed_sort_columns = ['id', 'title', 'text', 'user_id', 'category_id', 'is_locked', 'date_created', 'best_reply_id']

    if sort_by not in allowed_sort_columns:
        raise ValueError(f"Invalid sort column: {sort_by}")
    if order.upper() not in ["ASC", "DESC"]:
        raise ValueError(f"Invalid sort order: {order}")

    category_data = read_query(
        '''SELECT id, name, info, is_private, date_created, is_locked FROM categories WHERE id = ?''',
        (id,)
    )
    
    if not category_data:
        return None

    category = Category.from_query_result(*category_data[0])

    if category.is_private and user_id and not has_access(user_id, category.id, required_level=1):
        return None

    topic_query = '''
        SELECT id, title, text, user_id, category_id, is_locked, date_created, best_reply_id
        FROM topics WHERE category_id = ?
    '''
    params = [id]

    if search:
        topic_query += ' AND (title LIKE ? OR text LIKE ?)'
        like = f"%{search}%"
        params.extend([like, like])

    topic_query += f' ORDER BY {sort_by} {order.upper()}'

    topic_data = read_query(topic_query, tuple(params))
    category.topics = [Topic.from_query_result(*row) for row in topic_data]

    return category


def create_category(category: CategoryCreate, token: str):
    get_user_or_raise_401(token)
    if not category.name or category.name.strip() == "":
        raise ValueError("Category name is required.")

    new_id = insert_query('''INSERT INTO categories (name, info, is_private, date_created, is_locked) VALUES (?, ?, ?, ?, ?)''',
        (category.name, category.info, category.is_private, category.date_created, category.is_locked))

    data = read_query('''SELECT id, name, info, is_private, date_created, is_locked 
           FROM categories WHERE id = ?''', (new_id,))

    if new_id is None:
        raise ValueError("Failed to insert category into the database.")

    return next((Category.from_query_result(*row) for row in data), None)


def lock_category(category_id: int, token: str):
    user = get_user_or_raise_401(token)

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required to lock a category.")

    if category_id is None:
        raise HTTPException(status_code=400, detail="Category ID is required.")

    category = get_by_id(category_id, user.id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found.")
    if category == "no_write_access":
        raise HTTPException(status_code=403, detail="You do not have access to this category.")

    if not category.is_locked:
        updated_rows = update_query(
            '''UPDATE categories SET is_locked = 1 WHERE id = ?''',
            (category_id,)
        )
    if category.is_locked:
        updated_rows = update_query(
            '''UPDATE categories SET is_locked = 0 WHERE id = ?''',
            (category_id,))
            
        if updated_rows == 0:
            raise HTTPException(status_code=500, detail="Failed to lock the category due to a database error.")

    return get_by_id(category_id, user.id)


def get_private_categories():
    data = read_query('''SELECT id, name, info, is_private, date_created, is_locked
                         FROM categories 
                         WHERE is_private = 1''')
    return [Category.from_query_result(*row) for row in data]