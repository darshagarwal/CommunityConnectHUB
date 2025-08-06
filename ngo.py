from db import get_connection
from datetime import datetime

def register_ngo(user_id, name, email, cause):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ngos (user_id, name, email, cause) VALUES (%s, %s, %s, %s)",
                   (user_id, name, email, cause))
    conn.commit()
    conn.close()

def post_opportunity(ngo_id, title, description, skills_required, time_commitment, location, end_date, category):
    conn = get_connection()
    cursor = conn.cursor()
    start_date = datetime.now().strftime('%Y-%m-%d')  # Current date

    query = """
        INSERT INTO opportunities (ngo_id, title, description, skills_required, time_commitment,
        location, start_date, end_date, category)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (ngo_id, title, description, skills_required, time_commitment,
                           location, start_date, end_date, category))
    conn.commit()
    conn.close()
    print("✅ Opportunity posted successfully!")

def view_my_opportunities(ngo_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, description, start_date, end_date, location, category FROM opportunities WHERE ngo_id = %s", (ngo_id,))
    opportunities = cursor.fetchall()
    conn.close()

    if not opportunities:
        print("📭 No opportunities posted yet.")
        return

    print("\n📋 Your Posted Opportunities:")
    for opp in opportunities:
        print(f"🔹 Title: {opp[0]}")
        print(f"📝 Description: {opp[1]}")
        print(f"📅 Start: {opp[2]}, End: {opp[3]}")
        print(f"📍 Location: {opp[4]}, 🏷️ Category: {opp[5]}")
        print("-" * 40)

def view_applicants_for_ngo(ngo_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT o.title, s.name, s.email, s.skills
        FROM opportunities o
        JOIN student_interests_opportunities sio ON o.opportunity_id = sio.opportunity_id
        JOIN students s ON sio.student_id = s.student_id
        WHERE o.ngo_id = %s
        ORDER BY o.title
    """
    cursor.execute(query, (ngo_id,))
    results = cursor.fetchall()
    conn.close()

    if not results:
        print("📭 No students have applied to your opportunities yet.")
        return

    print("\n👥 Applicants for Your Opportunities:")
    current_title = None
    for row in results:
        title, name, email, skills = row
        if title != current_title:
            print(f"\n🔹 Opportunity: {title}")
            current_title = title
        print(f" - 👤 {name}, ✉️ {email}, 🧠 Skills: {skills}")
