from data.database import read_query, insert_query


def create_messages(sender_id, receiver_id, text):
    new_message = insert_query('INSERT INTO messages (sender_id, receiver_id, text) VALUES (?, ?, ?)', (sender_id, receiver_id, text))
    return {
        "id": new_message,
        "receiver_id": receiver_id,
        "sender_id": sender_id,
        "text": text
    }


def view_get_conversation(sender_id, receiver_id):
    view_con = read_query('SELECT * FROM messages WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?) ORDER BY created_at ASC', (sender_id, receiver_id, receiver_id, sender_id))
    return [{
        "id": t[0],
        "sender_id": t[1],
        "text": t[2],
        "date": t[3],
        "receiver_id": t[4],
    }
    for t in view_con
    ]


def view_conversations(id):
    all_chats = read_query('SELECT DISTINCT CASE WHEN sender_id = ? THEN receiver_id ELSE sender_id END AS other_user_id FROM messages WHERE sender_id = ? OR receiver_id = ? ', (id, id, id))
    result = []
    for i in all_chats:
        other_user = i[0]
        rows = read_query('SELECT id, username FROM users WHERE id = ?', (other_user, ))
        if rows:
            result.append({
                "id": rows[0][0],
                "username": rows[0][1]
            })
    return result