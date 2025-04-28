from data.database import read_query,insert_query
from data.models import Topics, TopicCreate,Replies


def get_all(search: str = None, sort: str = None):
    if search is None:
        data = read_query('''
            SELECT id, title, text, user_id, category_id, best_reply_id, date_created
            FROM topics
        ''')
    else:
        data = read_query('''
            SELECT id, title, text, user_id, category_id, best_reply_id, date_created
            FROM topics
            WHERE title LIKE ?
        ''', (f'%{search}%',))

    topics = []
    for row in data:
        topic = Topics.from_query_result(*row)
        
        replies_data = read_query(
            '''SELECT COUNT(*) FROM replies WHERE topic_id = ?''', (topic.id,)
        )
        replies_count = replies_data[0][0]

        topic.replies = replies_count

        topics.append(topic)

    if sort == 'asc':
        return sorted(topics, key=lambda t: t.date_create)
    elif sort == 'desc':
        return sorted(topics, key=lambda t: t.date_create, reverse=True)
    else:
        return topics


def get_by_id(id: int):
    data = read_query(
        '''SELECT id, title, text, user_id, category_id, best_reply_id
           FROM topics WHERE id = ?''', (id,))

    topic_row = next((row for row in data), None)
    if not topic_row:
        return None

    replies_data = read_query(
        '''SELECT id, text, date_created, date_updated, user_id, topic_id 
           FROM replies WHERE topic_id = ?''', (id,))

    replies = [Replies(
        id=row[0],
        text=row[1],
        date_create=row[2],
        date_update=row[3],
        user_id=row[4],
        topic_id=row[5]
    ) for row in replies_data]

    return Topics.from_query_result(*topic_row, replies=replies)

    
def create_topic(topic: TopicCreate, user_id: int):
    new_id = insert_query('''INSERT INTO topics (title,text, user_id, category_id) VALUES (?, ?, ?, ?)''',
        (topic.title,topic.text, user_id, topic.category_id))

    data = read_query('''SELECT id, title,text, user_id, category_id, best_reply_id 
           FROM topics WHERE id = ?''',(new_id,))

    return next((Topics.from_query_result(*row) for row in data), None)