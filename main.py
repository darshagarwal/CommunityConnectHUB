from auth import register_user, login_user
from student import register_student, list_opportunities, apply_to_opportunity, view_applied_opportunities
from ngo import register_ngo, post_opportunity, view_my_opportunities, view_applicants_for_ngo
from db import get_connection
from datetime import datetime
from ngo import record_volunteers_hours


def main():
    print("🌐 Welcome to Community Connect Hub")

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Choose a username: ")
            while True:
                password = input("Choose a password (min 8 characters): ")
                if len(password) < 8:
                    print("❌ Password must be at least 8 characters.")
                else:
                    break
            user_type = input("Are you registering as 'student' or 'ngo'? ").lower()

            if user_type not in ("student", "ngo"):
                print("❌ Invalid user type.")
                continue

            user_id = register_user(username, password, user_type)
            print("✅ Registered successfully!")

            if user_type == "student":
                name = input("Full Name: ")
                email = input("Email: ")
                skills = input("Skills (comma-separated): ")
                interests = input("Interests (comma-separated): ")
                register_student(user_id, name, email, skills, interests)

            elif user_type == "ngo":
                name = input("NGO Name: ")
                email = input("NGO Email: ")
                cause = input("Cause/Focus Area: ")
                register_ngo(user_id, name, email, cause)

        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            user = login_user(username, password)

            if not user:
                print("❌ Login failed.")
                continue

            user_id, user_type = user
            print(f"✅ Logged in as {user_type}")

            if user_type == "student":
                while True:
                    print("\n🎓 Student Menu")
                    print("1. View opportunities")
                    print("2. Apply to opportunity")
                    print("3. View my applications")
                    print("4. Logout")
                    student_choice = input("Select an option: ")

                    if student_choice == "1":
                        list_opportunities()

                    elif student_choice == "2":
                        opportunity_id = input("Enter Opportunity ID to apply: ")
                        apply_to_opportunity(user_id, opportunity_id)

                    elif student_choice == "3":
                        view_applied_opportunities(user_id)

                    elif student_choice == "4":
                        print("👋 Logged out.")
                        break

                    else:
                        print("❌ Invalid option.")

            elif user_type == "ngo":
                while True:
                    print("\n👤 NGO Menu")
                    print("1. Post a new opportunity")
                    print("2. View my posted opportunities")
                    print("3. View applicants for my opportunities")
                    print("4. Logout")
                    print("5. Record volunteer hours")
                    ngo_choice = input("Select an option: ")

                    if ngo_choice == "1":
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("SELECT ngo_id FROM ngos WHERE user_id = %s", (user_id,))
                        ngo = cursor.fetchone()
                        conn.close()

                        if not ngo:
                            print("❌ NGO profile not found.")
                            continue

                        ngo_id = ngo[0]
                        title = input("Enter opportunity title: ")
                        description = input("Enter description: ")
                        skills = input("Required skills: ")
                        time_commitment = input("Weekly time commitment (e.g., 5 hours/week): ")
                        location = input("Location: ")
                        end_date = input("Enter end date (YYYY-MM-DD): ")
                        category = input("Category (e.g., Education, Health): ")

                        try:
                            datetime.strptime(end_date, "%Y-%m-%d")
                            post_opportunity(ngo_id, title, description, skills, time_commitment, location, end_date, category)
                        except ValueError:
                            print("❌ Invalid end date format. Use YYYY-MM-DD.")

                    elif ngo_choice == "2":
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("SELECT ngo_id FROM ngos WHERE user_id = %s", (user_id,))
                        ngo = cursor.fetchone()
                        conn.close()

                        if ngo:
                            ngo_id = ngo[0]
                            view_my_opportunities(ngo_id)
                        else:
                            print("❌ NGO profile not found.")

                    elif ngo_choice == "3":
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("SELECT ngo_id FROM ngos WHERE user_id = %s", (user_id,))
                        ngo = cursor.fetchone()
                        conn.close()

                        if ngo:
                            ngo_id = ngo[0]
                            view_applicants_for_ngo(ngo_id)
                        else:
                            print("❌ NGO profile not found.")

                    elif ngo_choice == "4":
                        print("👋 Logged out.")
                        break
                    elif choice == "5":
                        record_volunteer_hours(ngo_id)

                    else:
                        print("❌ Invalid option.")

        elif choice == "3":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    main()
