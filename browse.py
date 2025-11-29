from db import get_connection
import datetime

def search_opportunities(keyword="", location="", category=""):
    conn = get_connection()
    cursor = conn.cursor()
    query = """SELECT opportunity_id, title, description, location, category 
               FROM opportunities 
               WHERE status = 'active'
               AND title LIKE %s AND location LIKE %s AND category LIKE %s"""
    cursor.execute(query, (f"%{keyword}%", f"%{location}%", f"%{category}%"))
    results = cursor.fetchall()
    conn.close()

    print("\n Search Results:")
    if not results:
        print("No opportunities found matching your search.")
    for row in results:
        print(f"[{row[0]}] {row[1]} | {row[2]} | {row[3]} | Category: {row[4]}")
    return results

def express_interest(student_id, opportunity_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """INSERT INTO student_interests_opportunities 
                   (student_id, opportunity_id, date_expressed_interest)
                   VALUES (%s, %s, %s)"""
        cursor.execute(query, (student_id, opportunity_id, datetime.datetime.now()))
        conn.commit()
        print(f"Student {student_id} expressed interest in opportunity {opportunity_id}")
    except Exception as e:
        print(" Already applied or error:", e)
    finally:
        conn.close()
