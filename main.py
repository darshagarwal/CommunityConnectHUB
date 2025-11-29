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

        elif choice=="2":
            u=input("Username: ")
            p=input("Password: ")
            res=login_user(u,p)
            if not res: print("❌ Invalid."); continue
            uid,ut=res
            print("Logged in as",ut)

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

            elif ut=="student":
                conn=get_connection()
                cur=conn.cursor()
                cur.execute("SELECT student_id FROM students WHERE user_id=%s",(uid,))
                row=cur.fetchone(); conn.close()
                if not row: print("No student profile."); continue
                sid=row[0]
                while True:
                    print("\nStudent Menu")
                    print("1.View opps\n2.Apply\n3.My apps\n4.Certificates\n5.Logout")
                    c=input("Choose: ")
                    if c=="1": view_opportunities()
                    elif c=="2": oid=int(input("Opp ID: ")); apply_for_opportunity(sid,oid)
                    elif c=="3": view_my_applications(sid)
                    elif c=="4": oid=int(input("Opp ID: ")); generate_certificate(sid,oid)
                    elif c=="5": break

        elif choice=="3": break

if __name__=="__main__":
    main()
