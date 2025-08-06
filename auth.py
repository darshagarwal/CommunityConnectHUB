from db import get_connection

def register_user(username, password, user_type):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("⚠️ Username already exists. Please choose another.")
        conn.close()
        return None

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
    return result  # (user_id, user_type) or None
