from db import get_connection

def register_user(username, password, user_type):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password, user_type))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, user_type FROM users WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result
