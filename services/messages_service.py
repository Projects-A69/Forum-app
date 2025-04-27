from data.database import read_query, insert_query, update_query
from data.models import Messages, Users

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

def create_message(sender_id, receiver_id, text):
    new_message = insert_query('INSERT INTO messages (sender_id, receiver_id, text) VALUES (?, ?, ?)', (sender_id, receiver_id, text))
    return {
        "id": new_message,
        "receiver_id": receiver_id,
        "sender_id": sender_id,
        "text": text
    }

def view_conversation(sender_id, receiver_id):
    view_con = read_query('SELECT * FROM messages WHERE sender_id = ? AND receiver_id = ? OR receiver_id = ? AND sender_id = ? ORDER BY created_at ASC', (sender_id, receiver_id, receiver_id, sender_id))
    return [{
        "receiver_id": t[0],
        "sender_id": t[1],
        "text": t[2],
        "date": t[3],
    }
    for t in view_con
    ]

def view_conversations(id: Users):
    all_conversation = read_query('SELECT DICTINCT u.id, u.username FROM users u JOIN (SELECT CASE)', (receiver_id, sender_id))