from data.database import read_query
from data.models import Messages

def all():
    rows = read_query('SELECT * FROM messages')
    return [{
             "id": row[0],
             "sender_id": row[1],
             "text": row[2],
             "created_at": row[3],
             "receiver_id": row[4]
             }
            for row in rows]

def get_by_id(id: int):
    rows = read_query('SELECT * FROM messages WHERE id = ?', (id,))
    return [{
             "id": row[0],
             "sender_id": row[1],
             "text": row[2],
             "created_at": row[3],
             "receiver_id": row[4]
             }
            for row in rows]