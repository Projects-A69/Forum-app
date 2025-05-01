from data.database import read_query, insert_query, update_query
from data.models import Reply, RepliesHasUsers, User
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

def vote_replies(users_id, replies_id, vote_type):
    is_exist_vote = read_query('SELECT vote_type FROM replies_has_votes WHERE users_id = ? AND replies_id = ?', (users_id, replies_id))
    if is_exist_vote:
        insert_query('UPDATE replies_has_votes SET vote_type = ? WHERE users_id = ? AND replies_id = ?',(vote_type, users_id, replies_id))
    else:
        insert_query('INSERT INTO replies_has_votes (users_id, replies_id, vote_type) VALUES (?, ?, ?)', (users_id, replies_id, vote_type))
    return get_vote_reply(replies_id)

def get_vote_reply(replies_id: int):
    result = read_query('SELECT (SELECT COUNT(*) FROM replies_has_votes WHERE replies_id = ? AND vote_type = 1) AS likes, (SELECT COUNT(*) FROM replies_has_votes WHERE replies_id = ? AND vote_type = 0)', (replies_id, replies_id))
    if result:
        likes, dislikes = result[0]
    else:
        likes, dislikes = 0, 0

    return {
        "id": replies_id,
        "likes": likes,
        "dislikes": dislikes
    }