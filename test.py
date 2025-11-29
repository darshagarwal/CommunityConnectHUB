import datetime
from auth import register_user, login_user
from ngo import (
    post_opportunity, view_my_opportunities, edit_opportunity,
    view_applicants, add_finance_entry, view_finance_report,
    assign_volunteer_hours, end_opportunity
)
from student import (
    view_opportunities, apply_for_opportunity,
    view_my_applications, generate_certificate
)
from db import get_connection

def run_all_tests():
    print("\n================= AUTH TESTS =================")
    try:
        student_uid = register_user("teststudent", "password123", "student")
        print("Registered new student, user_id:", student_uid)
    except Exception as e:
        print("Student already exists:", e)

    try:
        ngo_uid = register_user("testngo", "password123", "ngo")
        print("Registered new NGO, user_id:", ngo_uid)
    except Exception as e:
        print("NGO already exists:", e)

    print("Login student1:", login_user("student1", "password123"))
    print("Login ngo1:", login_user("ngo1", "password123"))

    print("\n================= NGO TESTS =================")
    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=5)

    post_opportunity(1, "School Cleanup", "Help clean school campus",
                     "Teamwork", "3 hours", "Delhi",
                     today, end_date, "Environment")

    view_my_opportunities(1)
    edit_opportunity(1, 1, title="Beach Clean-Up [Edited]")
    view_applicants(1)

    add_finance_entry(1, "collection", 10000, "Sponsor funding")
    add_finance_entry(1, "spending", 3500, "Event materials")
    view_finance_report(1)

    assign_volunteer_hours(1, 1, 7)
    end_opportunity(1, 1)

    print("\n================= STUDENT TESTS =================")
    view_opportunities()
    apply_for_opportunity(2, 2)
    view_my_applications(2)

    print("\n================= CERTIFICATE TESTS =================")
    generate_certificate(1, 1)
    generate_certificate(2, 2)

if __name__ == "__main__":
    with open("all_functions_output.txt", "w", encoding="utf-8") as f:
        import sys
        sys.stdout = f
        run_all_tests()
