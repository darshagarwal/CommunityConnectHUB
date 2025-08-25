from db import get_connection
from datetime import datetime

def view_all_opportunities():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT opportunity_id, title, category, start_date, end_date, location FROM opportunities WHERE status='active'")
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print("Available Opportunities:")
        for r in rows:
            print(f"{r[0]}. {r[1]} | {r[2]} | {r[3]} to {r[4]} | Location: {r[5]}")
    else:
        print("No active opportunities right now.")

def apply_to_opportunity(student_id, opportunity_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO student_interests_opportunities (student_id, opportunity_id, date_expressed_interest) VALUES (%s,%s,%s)"
    cursor.execute(query, (student_id, opportunity_id, datetime.now()))
    conn.commit()
    conn.close()
    print("✅ Your interest has been recorded. The NGO will contact you shortly.")

def view_my_applications(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """SELECT o.title, o.category, o.start_date, o.end_date
               FROM opportunities o
               JOIN student_interests_opportunities sio ON o.opportunity_id = sio.opportunity_id
               WHERE sio.student_id = %s"""
    cursor.execute(query, (student_id,))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print("📋 Your Applications:")
        for r in rows:
            print(f"- {r[0]} | {r[1]} | {r[2]} to {r[3]}")
    else:
        print("You haven’t applied for any opportunities yet.")
    
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
