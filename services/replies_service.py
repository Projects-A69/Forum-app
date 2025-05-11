from http.client import HTTPException

from services.category_access_service import has_access
from data.database import read_query, insert_query
from data.models import Reply, RepliesHasUsers, User, Topic, Category
from data.models import reply_votes


def create_replies(text, user_id, topic_id):
    topics = read_query('SELECT category_id, is_locked FROM topics WHERE id = ? ' ,(topic_id,))
    category_id, is_locked = topics[0]
    if is_locked:
        return 'topic is locked'
    categorys = read_query('SELECT is_private FROM categories WHERE id = ? ' ,(category_id,))
    is_private = categorys[0][0]
    if is_private and not has_access(user_id, category_id, required_level= 1):
        return "no_write_access"

    new_replies = insert_query('INSERT INTO replies (text, user_id, topic_id) VALUES (?, ?, ?)', (text, user_id, topic_id))
    return {
        "id": new_replies,
        "text": text,
        "user_id": user_id,
        "topic_id": topic_id
    }


def vote_replies(users_id, replies_id, vote_type):
    reply_existed = read_query('SELECT 1 FROM replies WHERE id = ? ' ,(replies_id,))
    if not reply_existed:
       return "Reply not found"
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