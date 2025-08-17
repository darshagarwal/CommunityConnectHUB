from db import get_connection
from datetime import datetime
from db import add_hours, set_hours, get_hours


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
        
def record_volunteer_hours(ngo_id):
    print("\n== Record Volunteer Hours ==")
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch all applicants for this NGO's opportunities
    cursor.execute("""
        SELECT sio.student_id, s.name, o.opportunity_id, o.title, sio.hours_worked
        FROM student_interests_opportunities sio
        JOIN students s ON s.student_id = sio.student_id
        JOIN opportunities o ON o.opportunity_id = sio.opportunity_id
        WHERE o.ngo_id = %s
    """, (ngo_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print("No students have applied to your opportunities yet.")
        return

    # Display applicants
    print("\nID | Student | Opportunity | Current Hours")
    for idx, (stu_id, stu_name, opp_id, opp_title, hrs) in enumerate(rows, start=1):
        print(f"{idx}. {stu_name} - {opp_title} ({hrs} hrs)")

    try:
        choice = int(input("\nSelect a number to update: "))
        if not (1 <= choice <= len(rows)):
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid input.")
        return

    stu_id, stu_name, opp_id, opp_title, hrs = rows[choice - 1]
    print(f"\nSelected {stu_name} on '{opp_title}' (current: {hrs} hrs)")

    mode = input("Enter 'a' to add hours or 's' to set total: ").lower()
    try:
        hours = int(input("Enter hours: "))
    except ValueError:
        print("Invalid hours.")
        return

    if mode == 'a':
        add_hours(stu_id, opp_id, hours)
        print(f"✅ Added {hours} hours. New total = {get_hours(stu_id, opp_id)}")
    elif mode == 's':
        set_hours(stu_id, opp_id, hours)
        print(f"✅ Hours set to {hours}.")
    else:
        print("Invalid option.")
