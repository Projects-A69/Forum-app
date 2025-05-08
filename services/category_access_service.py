from data.database import read_query, insert_query, update_query

def grant_access(user_id: int, category_id: int, access_level: int):
    result = read_query('''SELECT access_level FROM categories_has_users 
        WHERE users_id = ? AND categories_id = ?''',(user_id, category_id))

    if result:
        update_query('''UPDATE categories_has_users 
            SET access_level = ?
            WHERE users_id = ? AND categories_id = ?''',(access_level, user_id, category_id))
    else:
        insert_query('''
            INSERT INTO categories_has_users (categories_id, users_id, access_level)
            VALUES (?, ?, ?)''',(category_id, user_id, access_level))

def revoke_access(user_id: int, category_id: int):
    update_query('''DELETE FROM categories_has_users 
        WHERE users_id = ? AND categories_id = ?''',(user_id, category_id))

def get_category_access(category_id: int):
    rows = read_query('''SELECT u.id, u.username, chu.access_level 
        FROM categories_has_users chu
        JOIN users u ON chu.users_id = u.id
        WHERE chu.categories_id = ?''',(category_id,))

    return [{
            "user_id": row[0],
            "username": row[1],
            "access_level": row[2]}
        for row in rows]

def has_access(user_id: int, category_id: int, required_level: int) -> bool:
    result = read_query('''SELECT is_private FROM categories WHERE id = ?''', 
    (category_id,))

    if not result:
        return False

    is_private = result[0][0]

    if not is_private:
        return True  
    access = read_query('''SELECT access_level FROM categories_has_users 
        WHERE users_id = ? AND categories_id = ?''',(user_id, category_id))

    return access and access[0][0] >= required_level
