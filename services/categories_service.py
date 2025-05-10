from data.database import read_query, insert_query, update_query
from data.models import Category, CategoryCreate
from services.users_service import is_authenticated, from_token
from common.auth import get_user_or_raise_401

def get_all(search: str = None):
    if search is None:
        data = read_query('''SELECT id,name,info,is_private,date_created,is_locked FROM categories''')
    else:
        data = read_query('''SELECT id,name,info,is_private,date_created,is_locked FROM categories WHERE name LIKE ?''',
                          (f'%{search}%',))

    return (Category.from_query_result(*row) for row in data)


def get_by_id(id: int):
    data = read_query(
        '''SELECT id,name,info,is_private,date_created,is_locked FROM categories 
            WHERE id = ?''', (id,))
    
    # if data[0].is_private:
    #     if user_id and not has_access(user_id, id, 0): 
    #         return None

    return next((Category.from_query_result(*row) for row in data), None)


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


def view_categories():
    data = read_query('''SELECT id, name, info, is_private, date_created, is_locked FROM categories''')
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
