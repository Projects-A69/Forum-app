from data.database import read_query, insert_query, update_query
from data.models import Category, CategoryCreate
from common.auth import get_user_or_raise_401
from data.models import Topic
from services.category_access_service import has_access

def get_all(search: str = None):
    if search is None:
        data = read_query('''SELECT id,name,info,is_private,date_created,is_locked FROM categories''')
    else:
        data = read_query('''SELECT id,name,info,is_private,date_created,is_locked FROM categories WHERE name LIKE ?''',
                          (f'%{search}%',))

    return (Category.from_query_result(*row) for row in data)


def get_by_id(id: int, user_id:int):
    category_data = read_query('''SELECT id, name, info, is_private, date_created, is_locked FROM categories WHERE id = ?''', (id,))    
    if not category_data:
        return None
    
    category = Category.from_query_result(*category_data[0])

    if category.is_private and (user_id is None or not has_access(user_id, category.id, required_level=1)):
        return "no_write_access"

    topic_query = '''SELECT id, title, text, user_id, date_created FROM topics WHERE category_id = ?'''
    params = [id]

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

    if not new_id:
        raise ValueError("Failed to insert category into the database.")

    return next((Category.from_query_result(*row) for row in data), None)


def view_category(id: int, search: str = None, sort_by: str = "date_created", order: str = "ASC", page_size: int = 10,
                  page: int = 0):
    params = [id]
    query = '''SELECT id, name, info, is_private, date_created, is_locked
               FROM categories WHERE id = ?'''
    allowed_sort_columns = ['id', 'name', 'info', 'is_private', 'date_created', 'is_locked']

    if sort_by not in allowed_sort_columns:
        raise ValueError(f"Invalid sort column: {sort_by}")
    if order not in ["ASC", "DESC"]:
        raise ValueError(f"Invalid sort order: {order}")
    if search:
        query += ' AND name LIKE ?'
        params.append(f'%{search}%')

    query += f' ORDER BY {sort_by} {order}'
    query += ' LIMIT ? OFFSET ?'
    params.extend([page_size, page * page_size])

    data = read_query(query, tuple(params))
    return [Category.from_query_result(*row) for row in data]


def view_categories(search: str = None, sort: str = "desc", offset: int = 0, limit: int = 10):
    query = '''SELECT id, name, info, is_private, date_created, is_locked FROM categories WHERE 1 = 1'''
    params = []

    if search:
        query += ' AND (name LIKE ? OR info LIKE ?)'
        search_param = f'%{search}%'
        params.extend([search_param, search_param])

    query += f' ORDER BY date_created {sort.upper()}'

    query += ' LIMIT ? OFFSET ?'
    params.extend([limit, offset])

    data = read_query(query, tuple(params))
    return [Category.from_query_result(*row) for row in data]


def lock_category(category_id: int, token: str):
    user = get_user_or_raise_401(token)

    if not user.is_admin:
        raise ValueError("Admin access required to lock a category.")

    if category_id is None:
        raise ValueError("Category ID is required.")

    category = get_by_id(category_id)
    if category is None:
        return None

    if not category.is_locked:
        updated_rows = update_query('''UPDATE categories SET is_locked = 1 WHERE id = ?''', (category_id,))
        if updated_rows == 0:
            raise ValueError("Failed to lock the category due to a database error.")

    return get_by_id(category_id)

