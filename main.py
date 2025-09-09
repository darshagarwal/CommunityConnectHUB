from auth import register_user, login_user
from db import get_connection
from ngo import (
    post_opportunity, view_my_opportunities, edit_opportunity,
    view_applicants, add_finance_entry, view_finance_report,
    assign_volunteer_hours, end_opportunity
)
from student import (
    view_opportunities, apply_for_opportunity,
    view_my_applications, generate_certificate
)
import datetime

def main():
    print("🌍 Welcome to Community Connect Hub 🌍")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Select option: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password (min 8 chars): ")
            user_type = input("Type (student/ngo): ")
            try:
                user_id = register_user(username, password, user_type)
                print("✅ Registered successfully with user_id:", user_id)
            except Exception as e:
                print("❌ Error:", e)

        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            user = login_user(username, password)
            if not user:
                print("❌ Invalid credentials.")
                continue
            user_id, user_type = user
            print(f"✅ Logged in as {user_type}")

            if user_type == "ngo":
                while True:
                    print("\n👤 NGO Dashboard")
                    print("1. Post opportunity")
                    print("2. View my opportunities")
                    print("3. Edit opportunity")
                    print("4. View applicants")
                    print("5. Add finance entry")
                    print("6. View finance report")
                    print("7. Assign volunteer hours")
                    print("8. End opportunity early")
                    print("9. Logout")
                    ngo_choice = input("Choose: ")

                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT ngo_id FROM ngos WHERE user_id=%s", (user_id,))
                    ngo = cursor.fetchone()
                    conn.close()
                    if not ngo:
                        print("❌ NGO profile missing.")
                        break
                    ngo_id = ngo[0]

                    if ngo_choice == "1":
                        title = input("Title: ")
                        desc = input("Description: ")
                        skills = input("Required skills: ")
                        commitment = input("Time commitment: ")
                        location = input("Location: ")
                        start = datetime.date.today()
                        end = input("End date (YYYY-MM-DD): ")
                        category = input("Category: ")
                        post_opportunity(ngo_id, title, desc, skills, commitment, location, start, end, category)

                    elif ngo_choice == "2":
                        view_my_opportunities(ngo_id)

                    elif ngo_choice == "3":
                        oid = int(input("Opportunity ID: "))
                        new_title = input("New title: ")
                        edit_opportunity(ngo_id, oid, title=new_title)

                    elif ngo_choice == "4":
                        oid = int(input("Opportunity ID: "))
                        view_applicants(oid)

                    elif ngo_choice == "5":
                        t = input("Type (collection/spending): ")
                        amt = float(input("Amount: "))
                        desc = input("Description: ")
                        add_finance_entry(ngo_id, t, amt, desc)

                    elif ngo_choice == "6":
                        view_finance_report(ngo_id)

                    elif ngo_choice == "7":
                        sid = int(input("Student ID: "))
                        oid = int(input("Opportunity ID: "))
                        hrs = int(input("Hours: "))
                        assign_volunteer_hours(sid, oid, hrs)

                    elif ngo_choice == "8":
                        oid = int(input("Opportunity ID: "))
                        end_opportunity(ngo_id, oid)

                    elif ngo_choice == "9":
                        print("👋 Logged out.")
                        break

            elif user_type == "student":
                while True:
                    print("\n👤 Student Dashboard")
                    print("1. View opportunities")
                    print("2. Apply for opportunity")
                    print("3. View my applications")
                    print("4. View my certificates")
                    print("5. Logout")
                    st_choice = input("Choose: ")

                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT student_id FROM students WHERE user_id=%s", (user_id,))
                    student = cursor.fetchone()
                    conn.close()
                    if not student:
                        print("❌ Student profile missing.")
                        break
                    student_id = student[0]

                    if st_choice == "1":
                        view_opportunities()

                    elif st_choice == "2":
                        oid = int(input("Opportunity ID: "))
                        apply_for_opportunity(student_id, oid)

                    elif st_choice == "3":
                        view_my_applications(student_id)

                    elif st_choice == "4":
                        oid = int(input("Opportunity ID: "))
                        generate_certificate(student_id, oid)

                    elif st_choice == "5":
                        print("👋 Logged out.")
                        break

        elif choice == "3":
            print("👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
