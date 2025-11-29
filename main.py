from auth import register_user, login_user
from db import get_connection, create_tables
from ngo import (
    post_opportunity, view_my_opportunities, edit_opportunity,
    view_applicants, add_finance_entry, view_impact_report,
    assign_volunteer_hours, end_opportunity
)
from student import (
    view_opportunities, apply_for_opportunity,
    view_my_applications, generate_certificate
)
import datetime

def main():
    create_tables()
    print("🌍 Welcome to Community Connect Hub 🌍")

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice=input("Choose: ")

        if choice=="1":
            u=input("Username: ")
            p=input("Password (min 8 chars): ")
            t=input("Type (student/ngo): ")
            if len(p)<8: print("❌ Password too short."); continue
            try:
                uid=register_user(u,p,t)
                print("✅ Registered with ID",uid)
            except Exception as e: print("Error:",e)

        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            user = login_user(username, password)
            if not user:
                print("Invalid credentials.")
                continue
            user_id, user_type = user
            print(f"Logged in as {user_type}")

            if ut=="ngo":
                conn=get_connection()
                cur=conn.cursor()
                cur.execute("SELECT ngo_id FROM ngos WHERE user_id=%s",(uid,))
                row=cur.fetchone()
                conn.close()
                if not row: print("No NGO profile."); continue
                ngo_id=row[0]
                while True:
                    print("\nNGO Menu")
                    print("1.Post opp\n2.View opps\n3.Edit opp\n4.View applicants")
                    print("5.Add finance\n6.View impact\n7.Assign hours\n8.End opp\n9.Logout")
                    c=input("Choose: ")
                    if c=="1":
                        t=input("Title: "); d=input("Desc: "); s=input("Skills: ")
                        comm=input("Commitment: "); loc=input("Location: ")
                        end=input("End date YYYY-MM-DD: "); cat=input("Category: ")
                        post_opportunity(ngo_id,t,d,s,comm,loc,datetime.date.today(),end,cat)
                    elif c=="2": view_my_opportunities(ngo_id)
                    elif c=="3": oid=int(input("Opp ID: ")); new=input("New title: "); edit_opportunity(ngo_id,oid,title=new)
                    elif c=="4": oid=int(input("Opp ID: ")); view_applicants(oid)
                    elif c=="5": oid=int(input("Opp ID: ")); typ=input("collection/spending: "); amt=float(input("Amt: ")); desc=input("Desc: "); add_finance_entry(ngo_id,oid,typ,amt,desc)
                    elif c=="6": view_impact_report(ngo_id)
                    elif c=="7": sid=int(input("Student ID: ")); oid=int(input("Opp ID: ")); h=int(input("Hours: ")); assign_volunteer_hours(sid,oid,h)
                    elif c=="8": oid=int(input("Opp ID: ")); end_opportunity(ngo_id,oid)
                    elif c=="9": break

                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT ngo_id FROM ngos WHERE user_id=%s", (user_id,))
                    ngo = cursor.fetchone()
                    conn.close()
                    if not ngo:
                        print("NGO profile missing.")
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
                        oid = int(input("Opportunity ID: "))
                        t = input("Type (collection/spending): ")
                        amt = float(input("Amount: "))
                        desc = input("Description: ")
                        add_finance_entry(ngo_id, oid, t, amt, desc)

                    elif ngo_choice == "6":
                        view_impact_report(ngo_id)

                    elif ngo_choice == "7":
                        sid = int(input("Student ID: "))
                        oid = int(input("Opportunity ID: "))
                        hrs = int(input("Hours: "))
                        assign_volunteer_hours(sid, oid, hrs)

                    elif ngo_choice == "8":
                        oid = int(input("Opportunity ID: "))
                        end_opportunity(ngo_id, oid)

                    elif ngo_choice == "9":
                        print("Logged out.")
                        break

            elif user_type == "student":
                while True:
                    print("\n Student Dashboard")
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
                        print("Student profile missing.")
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
                        print("Logged out.")
                        break

        elif choice == "3":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
