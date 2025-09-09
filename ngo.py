from db import get_connection
import datetime

def post_opportunity(ngo_id, title, desc, skills, commitment, location, start_date, end_date, category):
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO opportunities 
    (ngo_id, title, description, required_skills, time_commitment, location, start_date, end_date, category, status)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'active')"""
    cursor.execute(query, (ngo_id, title, desc, skills, commitment, location, start_date, end_date, category))
    conn.commit()
    conn.close()
    print("✅ Opportunity posted successfully!")

def view_my_opportunities(ngo_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT opportunity_id, title, status, start_date, end_date FROM opportunities WHERE ngo_id=%s", (ngo_id,))
    rows = cursor.fetchall()
    conn.close()
    print("\n📌 Opportunities by NGO", ngo_id)
    for row in rows:
        print(f"[{row[0]}] {row[1]} | {row[2]} | {row[3]} → {row[4]}")

def edit_opportunity(ngo_id, opportunity_id, **updates):
    conn = get_connection()
    cursor = conn.cursor()
    set_clause = ", ".join(f"{col}=%s" for col in updates.keys())
    values = list(updates.values()) + [ngo_id, opportunity_id]
    query = f"UPDATE opportunities SET {set_clause} WHERE ngo_id=%s AND opportunity_id=%s"
    cursor.execute(query, tuple(values))
    conn.commit()
    conn.close()
    print(f"✅ Opportunity {opportunity_id} updated!")

def view_applicants(opportunity_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT s.student_id, s.name, s.contact_email, s.interests
    FROM students s
    JOIN student_interests_opportunities sio ON s.student_id = sio.student_id
    WHERE sio.opportunity_id = %s
    """
    cursor.execute(query, (opportunity_id,))
    rows = cursor.fetchall()
    conn.close()
    print(f"\n📌 Applicants for Opportunity {opportunity_id}:")
    for row in rows:
        print(f"Student {row[0]}: {row[1]} | {row[2]} | Interests: {row[3]}")

def add_finance_entry(ngo_id, opportunity_id, entry_type, amount, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ngo_finance (ngo_id, opportunity_id, type, amount, description, date) VALUES (%s,%s,%s,%s,%s,%s)",
        (ngo_id, opportunity_id, entry_type, amount, description, datetime.date.today())
    )
    conn.commit()
    conn.close()
    print(f"✅ Finance entry added for opportunity {opportunity_id}.")

def view_impact_report(ngo_id):
    conn = get_connection()
    cursor = conn.cursor()

    print(f"\n📊 Impact Report for NGO {ngo_id}")

    # Get all opportunities of this NGO
    cursor.execute("SELECT opportunity_id, title FROM opportunities WHERE ngo_id=%s", (ngo_id,))
    opportunities = cursor.fetchall()

    if not opportunities:
        print("❌ No opportunities found for this NGO.")
        conn.close()
        return

    for opp in opportunities:
        opp_id, title = opp
        print(f"\n🚩 Opportunity: {title} (ID: {opp_id})")

        # Finance records
        cursor.execute("""
        SELECT type, amount, description, date 
        FROM ngo_finance 
        WHERE ngo_id=%s AND opportunity_id=%s
        """, (ngo_id, opp_id))
        finances = cursor.fetchall()
        print("\n💰 Finance Records:")
        if not finances:
            print("   No finance records yet.")
        for row in finances:
            print(f"   {row[0]} | ₹{row[1]} | {row[2]} | {row[3]}")

        # Volunteer hours
        cursor.execute("""
        SELECT s.name, v.hours 
        FROM volunteer_hours v
        JOIN students s ON v.student_id = s.student_id
        WHERE v.opportunity_id=%s
        """, (opp_id,))
        hours = cursor.fetchall()
        print("\n⏱ Volunteer Hours:")
        if not hours:
            print("   No volunteer hours assigned yet.")
        for row in hours:
            print(f"   {row[0]} → {row[1]} hours")

    conn.close()

def assign_volunteer_hours(student_id, opportunity_id, hours):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO volunteer_hours (student_id, opportunity_id, hours) VALUES (%s,%s,%s) "
                   "ON DUPLICATE KEY UPDATE hours=%s", (student_id, opportunity_id, hours, hours))
    conn.commit()
    conn.close()
    print(f"✅ Assigned {hours} hours to student {student_id} for opportunity {opportunity_id}")

def end_opportunity(ngo_id, opportunity_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE opportunities SET status='ended' WHERE ngo_id=%s AND opportunity_id=%s", (ngo_id, opportunity_id))
    conn.commit()
    conn.close()
    print(f"✅ Opportunity {opportunity_id} has been ended early by NGO {ngo_id}.")
