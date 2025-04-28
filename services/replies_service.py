from data.database import read_query, insert_query, update_query
from data.models import Replies, RepliesHasUsers, Users
from data.models import reply_votes


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
    vote_reply = read_query('SELECT user_id, reply_id, vote_type FROM replies_has_users WHERE user_id = ? AND reply_id = ?', (user_id, reply_id))
    if vote_reply:
        insert_query('UPDATE replies_has_users SET vote_type = ? WHERE user_id = ? AND reply_id = ?', (vote_type, user_id, reply_votes))
    else:
        insert_query('INSERT INTO replies_has_users (user_id, reply_id, reply_type) VALUES (?, ?, ?)', (user_id, reply_id, vote_type))
    return {
        "user_id": user_id,
        "reply_id": reply_id,
        "vote_type": vote_type,
    }

def best_replies():
    NotImplemented()