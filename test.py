from db import create_tables, get_connection
from auth import register_user
from ngo import (
    post_opportunity, view_my_opportunities, view_applicants,
    add_finance_entry, view_impact_report,
    assign_volunteer_hours, end_opportunity
)
from student import (
    view_opportunities, apply_for_opportunity,
    view_my_applications, generate_certificate
)
import datetime
import sys

# Redirect output to file
sys.stdout = open("test_output.txt", "w", encoding="utf-8")

def reset_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    for tbl in ["volunteer_hours","ngo_finance","student_interests_opportunities",
                "opportunities","students","ngos","users"]:
        cur.execute(f"TRUNCATE TABLE {tbl}")
    cur.execute("SET FOREIGN_KEY_CHECKS=1")
    conn.commit()
    conn.close()

def seed_data():
    ngo_uid = register_user("ngo_demo", "password123", "ngo")
    stu_uid = register_user("stu_demo", "password123", "student")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""INSERT INTO ngos (user_id,name,mission_statement,address,contact_person,contact_email)
                   VALUES (%s,%s,%s,%s,%s,%s)""",
                (ngo_uid,"Helping Hands","We serve","Delhi","Anita","ngo@example.com"))
    ngo_id = cur.lastrowid

    cur.execute("""INSERT INTO students (user_id,name,grade,contact_email,interests)
                   VALUES (%s,%s,%s,%s,%s)""",
                (stu_uid,"Riya",11,"riya@example.com","Environment, Teaching"))
    student_id = cur.lastrowid
    conn.commit()
    conn.close()
    return ngo_id, student_id

def run_tests():
    create_tables()
    reset_db()
    ngo_id, stu_id = seed_data()

    print("🌍 Welcome to Community Connect Hub 🌍")

    # Main menu -> NGO login
    print("\nMain Menu:\n1. Register\n2. Login\n3. Exit")
    print("👉 User selects: 2 (Login)")
    print("Username: ngo_demo")
    print("Password: password123")
    print("✅ Logged in as NGO")

    # NGO Menu
    print("\n👤 NGO Menu\n1. Post a new opportunity\n2. View my posted opportunities\n"
          "3. Edit an opportunity\n4. View applicants\n5. Add finance\n6. View impact\n"
          "7. Assign hours\n8. End opportunity\n9. Logout")
    print("👉 User selects: 1 (Post new opportunity)")
    post_opportunity(ngo_id,"Tree Plantation","Plant trees in park","Gardening",
                     "2 hours/week","Delhi",datetime.date.today(),
                     datetime.date.today()+datetime.timedelta(days=7),"Environment")

    print("\n👉 User selects: 2 (View my posted opportunities)")
    view_my_opportunities(ngo_id)

    # Logout NGO -> Student Login
    print("\n👉 User selects: 9 (Logout)")

    print("\nMain Menu:\n1. Register\n2. Login\n3. Exit")
    print("👉 User selects: 2 (Login)")
    print("Username: stu_demo")
    print("Password: password123")
    print("✅ Logged in as Student")

    # Student Menu
    print("\n👤 Student Menu\n1. View available opportunities\n2. Apply\n3. My apps\n"
          "4. Certificates\n5. Logout")
    print("👉 User selects: 1 (View opportunities)")
    view_opportunities()

    print("\n👉 User selects: 2 (Apply for opportunity 1)")
    apply_for_opportunity(stu_id,1)

    print("\n👉 User selects: 3 (My Applications)")
    view_my_applications(stu_id)

    print("\n👉 User selects: 5 (Logout)")

    # NGO logs back in
    print("\nMain Menu:\n1. Register\n2. Login\n3. Exit")
    print("👉 User selects: 2 (Login)")
    print("Username: ngo_demo")
    print("Password: password123")
    print("✅ Logged in as NGO")

    print("\n👉 User selects: 4 (View applicants for opp 1)")
    view_applicants(1)

    print("\n👉 User selects: 5 (Add finance entries)")
    add_finance_entry(ngo_id,1,"collection",5000,"CSR donation")
    add_finance_entry(ngo_id,1,"spending",2000,"Saplings purchase")

    print("\n👉 User selects: 6 (View impact report)")
    view_impact_report(ngo_id)

    print("\n👉 User selects: 7 (Assign volunteer hours)")
    assign_volunteer_hours(stu_id,1,10)

    print("\n👉 User selects: 8 (End opportunity)")
    end_opportunity(ngo_id,1)

    print("\n👉 User selects: 9 (Logout)")

    # Student views certificate
    print("\nMain Menu:\n1. Register\n2. Login\n3. Exit")
    print("👉 User selects: 2 (Login)")
    print("Username: stu_demo")
    print("Password: password123")
    print("✅ Logged in as Student")

    print("\n👉 User selects: 4 (Certificates)")
    generate_certificate(stu_id,1)

    print("\n👉 User selects: 5 (Logout)")
    print("\n👋 Session ended")

if __name__=="__main__":
    run_tests()
    print("\n✅ Test session completed. Open test_output.txt for the simulated terminal log.")
