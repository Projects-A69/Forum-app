from data.database import read_query,insert_query
from data.models import Topics, TopicCreate


def get_all(search: str = None):
    if search is None:
        data = read_query('''SELECT id,title,user_id,category_id,best_reply_id FROM topics''')
    else:
        data = read_query('''SELECT id,title,user_id,category_id,best_reply_id FROM topics WHERE title LIKE ?''', (f'%{search}%',))
        
    return (Topics.from_query_result(*row) for row in data)

def get_by_id(id: int):
    data = read_query(
        '''SELECT id, title, user_id, category_id, best_reply_id FROM topics 
            WHERE id = ?''', (id,))

    return next((Topics.from_query_result(*row) for row in data), None)
    
def create_topic(topic: TopicCreate, user_id: int):
    new_id = insert_query('''INSERT INTO topics (title,text, user_id, category_id) VALUES (?, ?, ?, ?)''',
        (topic.title,topic.text, user_id, topic.category_id))

    data = read_query('''SELECT id, title,text, user_id, category_id, best_reply_id 
           FROM topics WHERE id = ?''',(new_id,))

    return next((Topics.from_query_result(*row) for row in data), None)