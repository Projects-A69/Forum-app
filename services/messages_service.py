from data.database import read_query, insert_query
from data.models import Message, User


def create_messages(sender_id, receiver_id, text):
    new_message = insert_query('INSERT INTO messages (sender_id, receiver_id, text) VALUES (?, ?, ?)', (sender_id, receiver_id, text))
    return {
        "id": new_message,
        "receiver_id": receiver_id,
        "sender_id": sender_id,
        "text": text
    }


def view_get_conversation(sender_id, receiver_id):
    view_con = read_query('SELECT * FROM messages WHERE sender_id = ? AND receiver_id = ? OR receiver_id = ? AND sender_id = ? ORDER BY created_at ASC', (sender_id, receiver_id, receiver_id, sender_id))
    return [{
        "receiver_id": t[0],
        "sender_id": t[1],
        "text": t[2],
        "date": t[3],
    }
    for t in view_con
    ]


def view_conversations(id):
    all_chats = read_query('SELECT * FROM messages WHERE sender_id = ? OR receiver_id = ? ', (id, id))
    all_users = set()
    for chat in all_chats:
        sender_id = chat[0]
        receiver_id = chat[1]
        if sender_id == id:
            all_users.add(receiver_id)
        if receiver_id == id:
            all_users.add(sender_id)
    if all_users:
        placeholders_users = ', '.join(['?'] * len(all_users))
        q_users = f'SELECT id, username FROM users WHERE id in ({placeholders_users})'
        users = read_query(q_users, tuple(all_users))
        return [{
            'user_id': c[0],
            'username': c[1]
            }
        for c in users
            ]
    else:
        return []