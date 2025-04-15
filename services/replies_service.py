from data.database import read_query
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