from data.database import read_query, insert_query, update_query
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

def create_message(receiver_id, text):
    new_message = insert_query('INSERT INTO messages (receiver_id, text) VALUES (?, ?)', (receiver_id, text))
    return {
        "id": new_message["id"],
        "receiver_id": receiver_id,
        "text": text
    }