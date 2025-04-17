#Uasim
from data.database import read_query
from data.models import Topics


def get_all(search: str = None):
    if search is None:
        data = read_query('''SELECT id,title,user_id,category_id,best_reply_id FROM topics''')
    else:
        data = read_query('''SELECT id,title,user_id,category_id,best_reply_id FROM topics WHERE title LIKE ?''', (f'%{search}%',))
        
    return (Topics.from_query_result(*row) for row in data)
    