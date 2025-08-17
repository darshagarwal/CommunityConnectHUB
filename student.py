from db import get_connection

def register_student(user_id, name, grade, email, phone, interests):
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO students (user_id, name, grade, contact_email, contact_phone, interests)
               VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (user_id, name, grade, email, phone, interests))
    conn.commit()
    conn.close()
    
def view_my_hours(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.title, sio.hours_worked
        FROM student_interests_opportunities sio
        JOIN opportunities o ON o.opportunity_id = sio.opportunity_id
        WHERE sio.student_id = %s
    """, (student_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    print("\n== My Volunteer Hours ==")
    if not rows:
        print("You have not applied for any opportunities yet.")
        return

    for title, hrs in rows:
        print(f"{title} → {hrs} hours")
