from data.database import read_query,insert_query
from data.models import Topic, TopicCreate,Reply
from services.category_access_service import has_access



def get_all(search: str = None, sort: str = None):
    if search is None:
        data = read_query('''SELECT id, title, text, user_id, category_id, best_reply_id, date_created
            FROM topics''')
    else:
        data = read_query('''SELECT id, title, text, user_id, category_id, best_reply_id, date_created
            FROM topics
            WHERE title LIKE ?''', (f'%{search}%',))

    topics = []
    for row in data:
        topic = Topic.from_query_result(*row)
        
        replies_data = read_query('''SELECT id, text, date_created, date_updated, user_id, topic_id
            FROM replies
            WHERE topic_id = ?''', (topic.id,))
        topic.replies = [Reply.from_query_result(*reply_row) for reply_row in replies_data]
        topics.append(topic)

    if sort == 'asc':
        return sorted(topics, key=lambda t: t.date_create)
    elif sort == 'desc':
        return sorted(topics, key=lambda t: t.date_create, reverse=True)
    else:
        return topics


def get_by_id(id: int):
    data = read_query('''SELECT id, title, text, user_id, category_id, best_reply_id
           FROM topics WHERE id = ?''', (id,))

    topic_row = next((row for row in data), None)
    if not topic_row:
        return None

    replies_data = read_query('''SELECT id, text, date_created, date_updated, user_id, topic_id 
           FROM replies WHERE topic_id = ?''', (id,))

    replies = [Reply(
        id=row[0],
        text=row[1],
        date_create=row[2],
        date_update=row[3],
        user_id=row[4],
        topic_id=row[5]
    ) for row in replies_data]

    return Topic.from_query_result(*topic_row, replies=replies)

    
def create_topic(topic: TopicCreate, user_id: int):
    category = read_query('''SELECT is_private, is_locked FROM categories WHERE id = ?''', 
                          (topic.category_id,))
    
    if not category:
        return "category_not_found"

    is_private, is_locked = category[0]

    if is_locked:
        return "category_locked"

    if is_private and not has_access(user_id, topic.category_id, required_level=1):
        return "no_write_access"

    new_id = insert_query('''INSERT INTO topics (title, text, user_id, category_id) 
                             VALUES (?, ?, ?, ?)''',
                          (topic.title, topic.text, user_id, topic.category_id))

    data = read_query('''SELECT id, title, text, user_id, category_id, best_reply_id 
                         FROM topics WHERE id = ?''', (new_id,))

    return next((Topic.from_query_result(*row) for row in data), None)

def lock_topic(topic_id: int) -> bool:
    topic = get_by_id(topic_id)
    if topic is None:
        return None

    insert_query('''UPDATE topics SET is_locked = 1 WHERE id = ?''', (topic_id,))

    updated = read_query('''SELECT id, title, description, user_id, is_locked, best_reply_id 
           FROM topics 
           WHERE id = ?''', (topic_id,))

    return Topic.from_query_result(*updated[0]) if updated else None


def choose_best_reply(topic_id: int, reply_id: int, user_id: int) -> str | None:
    topic = get_by_id(topic_id)
    if topic is None:
        return "topic_not_found"

    if topic.user_id != user_id:
        return "not_author"

    reply_check = read_query('''SELECT id FROM replies WHERE id = ? AND topic_id = ?''', (reply_id, topic_id))
    if not reply_check:
        return "reply_not_found"

    insert_query('''UPDATE topics SET best_reply_id = ? WHERE id = ?''', (reply_id, topic_id))
    
    return get_topic_with_replies(topic_id)


def get_topic_with_replies(topic_id: int) -> Topic | None:
    data = read_query('''SELECT id, title, text, user_id, category_id, is_locked, date_created, best_reply_id
        FROM topics
        WHERE id = ?''', (topic_id,))

    if not data:
        return None

    topic = Topic.from_query_result(*data[0])

    replies_data = read_query('''SELECT id, text, date_created, date_updated, user_id, topic_id
        FROM replies
        WHERE topic_id = ?
        ORDER BY date_created  # Optional: Sort by newest/oldest''', (topic_id,))

    topic.replies = [Reply.from_query_result(*row) for row in replies_data]

    return topic