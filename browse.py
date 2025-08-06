from db import get_connection

def search_opportunities(keyword="", location="", category=""):
    conn = get_connection()
    cursor = conn.cursor()
    query = """SELECT opportunity_id, title, description, location, category FROM opportunities 
               WHERE status = 'active' AND
               title LIKE %s AND location LIKE %s AND category LIKE %s"""
    cursor.execute(query, (f"%{keyword}%", f"%{location}%", f"%{category}%"))
    results = cursor.fetchall()
    conn.close()
    return results

def express_interest(student_id, opportunity_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO student_interests_opportunities (student_id, opportunity_id)
               VALUES (%s, %s)"""
    cursor.execute(query, (student_id, opportunity_id))
    conn.commit()
    conn.close()
