from db import get_connection
import datetime

def view_opportunities():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT opportunity_id, title, description, location, start_date, end_date, status FROM opportunities WHERE status='active'")
    rows = cursor.fetchall()
    conn.close()
    print("\n Available Opportunities:")
    for row in rows:
        print(f"[{row[0]}] {row[1]} | {row[2]} | {row[3]} | {row[4]} → {row[5]} | {row[6]}")

def apply_for_opportunity(student_id, opportunity_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO student_interests_opportunities (student_id, opportunity_id, date_expressed_interest) VALUES (%s,%s,NOW())",
                       (student_id, opportunity_id))
        conn.commit()
        print(f"Student {student_id} applied for opportunity {opportunity_id}")
    except Exception as e:
        print(" Already applied or error:", e)
    conn.close()

def view_my_applications(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT o.opportunity_id, o.title, o.location, o.start_date, o.end_date, o.status
    FROM opportunities o
    JOIN student_interests_opportunities sio ON o.opportunity_id = sio.opportunity_id
    WHERE sio.student_id = %s
    """
    cursor.execute(query, (student_id,))
    rows = cursor.fetchall()
    conn.close()
    print(f"\n Applications of Student {student_id}:")
    for row in rows:
        print(f"[{row[0]}] {row[1]} | {row[2]} | {row[3]} → {row[4]} | {row[5]}")

# ---------------- CERTIFICATE LOGIC ---------------- #

def generate_certificate(student_id, opportunity_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch opportunity details
    cursor.execute("SELECT title, end_date, status FROM opportunities WHERE opportunity_id = %s", (opportunity_id,))
    opp = cursor.fetchone()
    if not opp:
        print(" Opportunity not found.")
        conn.close()
        return

    title, end_date, status = opp
    today = datetime.date.today()

    if status != "ended" and today < end_date:
        print(" Certificate not available yet. Opportunity is still ongoing.")
        conn.close()
        return

    cursor.execute("SELECT hours FROM volunteer_hours WHERE student_id=%s AND opportunity_id=%s",
                   (student_id, opportunity_id))
    hours = cursor.fetchone()
    if not hours:
        print(" NGO has not assigned hours yet. Certificate not available.")
        conn.close()
        return

    hours = hours[0]

    cursor.execute("SELECT name FROM students WHERE student_id=%s", (student_id,))
    student = cursor.fetchone()
    conn.close()

    if not student:
        print(" Student not found.")
        return

    student_name = student[0]
    print("\n" + "="*70)
    print("|" + "🎖️  VOLUNTEER CERTIFICATE  🎖️".center(68) +"  " + "|")
    print("="*70)
    print("|" + " ".center(68) + "|")
    print("|" + "This is to proudly certify that".center(68) + "|")
    print("|" + " ".center(68) + "|")
    
    print("|" + f"{student_name.upper()}".center(65) + '   '+"|")
    print("|" + " ".center(68) + "|")
    
    print("|" + "has successfully contributed:".center(68) + "|")
    print("|" + " ".center(68) + "|")
    
    print("|" + f"➤ {hours} HOURS of dedicated volunteer service".center(68) + "|")
    print("|" + " ".center(68) + "|")
    
    print("|" + "during the opportunity:".center(68) + "|")
    print("|" + " ".center(68) + "|")
    
    print("|" + f" \"{title}\"".center(68) + "|")
    print("|" + " ".center(68) + "|")
    
    print("|" + f"Successfully completed on: {end_date}".center(68) + "|")
    print("|" + " ".center(68) + "|")
    
    print("|" + "We appreciate your commitment towards community welfare!".center(68) + "|")
    print("|" + " ".center(68) + "|")
    
    print("="*70)
    print("|" + "— Community Connect Hub —".center(68) + "|")
    print("="*70 + "\n")
