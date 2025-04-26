from data.database import read_query, insert_query, update_query
from data.models import Replies

def get_all():
    rows = read_query('SELECT * FROM replies')
    return [{
        "id": row[0],
        "text": row[1],
        "date_create": row[2],
        "date_update": row[3],
        "user_id": row[4],
        "topic_id": row[5]
    }]

def get_by_id(id: int):
    rows = read_query('SELECT * FROM replies WHERE id=?', (id,))
    return [{
        "id": row[0],
        "text": row[1],
        "date_create": row[2],
        "date_update": row[3],
        "user_id": row[4],
        "topic_id": row[5]
    }]

def create_replies(text, user_id, topic_id):
    new_replies = insert_query('INSERT INTO replies (text, user_id, topic_id) VALUES (?, ?, ?)', (text, user_id, topic_id))
    return {
        "id": new_replies,
        "text": text,
        "user_id": user_id,
        "topic_id": topic_id
    }

def vote_replies():
    NotImplemented()

def best_replies():
    NotImplemented()