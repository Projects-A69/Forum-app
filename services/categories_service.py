from data.database import read_query, insert_query, update_query
from data.models import Category, CategoryCreate


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

    return next((Category.from_query_result(*row) for row in data), None)

def create_category(category: CategoryCreate):
    new_id = insert_query('''INSERT INTO categories (name, info, is_private, date_created, is_locked) VALUES (?, ?, ?, ?, ?)''',
        (category.name,category.info, category.date_created,))

    data = read_query('''SELECT id,name,info,is_private,date_created,is_locked 
           FROM topics WHERE id = ?''',(new_id,))

    return next((Category.from_query_result(*row) for row in data), None)
