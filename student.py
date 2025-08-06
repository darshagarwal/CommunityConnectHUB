from db import get_connection

def register_student(user_id, name, grade, email, phone, interests):
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO students (user_id, name, grade, contact_email, contact_phone, interests)
               VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (user_id, name, grade, email, phone, interests))
    conn.commit()
    conn.close()
