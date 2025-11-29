from db import get_connection

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Clear old data so it's repeatable
    tables = [
        "volunteer_hours",
        "ngo_finance",
        "student_interests_opportunities",
        "opportunities",
        "students",
        "ngos",
        "users"
    ]
    for t in tables:
        cursor.execute(f"DELETE FROM {t}")

    # Users
    cursor.executemany(
        "INSERT INTO users (username, password, user_type) VALUES (%s,%s,%s)",
        [
            ('student1','password123','student'),
            ('student2','password123','student'),
            ('student3','password123','student'),
            ('student4','password123','student'),
            ('student5','password123','student'),
            ('student6','password123','student'),
            ('student7','password123','student'),
            ('student8','password123','student'),
            ('ngo1','password123','ngo'),
            ('ngo2','password123','ngo'),
            ('ngo3','password123','ngo')
        ]
    )

    # Students
    cursor.executemany(
        "INSERT INTO students (user_id, name, grade, contact_email, interests) VALUES (%s,%s,%s,%s,%s)",
        [
            (1,'Riya Mehra',11,'riya@example.com','Environment, Teaching'),
            (2,'Arjun Singh',12,'arjun@example.com','Animals, Healthcare'),
            (3,'Neha Sharma',11,'neha@example.com','Education, Tutoring'),
            (4,'Kabir Das',12,'kabir@example.com','Environment, Music'),
            (5,'Sanya Kapoor',10,'sanya@example.com','Healthcare, Reading'),
            (6,'Rahul Jain',11,'rahul@example.com','Sports, Animals'),
            (7,'Ishita Roy',12,'ishita@example.com','Teaching, Coding'),
            (8,'Aman Khan',10,'aman@example.com','Environment, Art')
        ]
    )

    # NGOs
    cursor.executemany(
        "INSERT INTO ngos (user_id, name, mission_statement, address, contact_person, contact_email) VALUES (%s,%s,%s,%s,%s,%s)",
        [
            (9,'Green Earth','Protecting environment and organizing cleanups','Delhi','Meena Gupta','greenearth@example.com'),
            (10,'Animal Care','Helping street animals find homes','Mumbai','Rohit Sen','animalcare@example.com'),
            (11,'EduHelp','Tutoring underprivileged kids','Kolkata','Priya Nair','eduhelp@example.com')
        ]
    )

    # Opportunities
    cursor.executemany(
        "INSERT INTO opportunities (ngo_id, title, description, required_skills, time_commitment, location, start_date, end_date, status, category) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        [
            (1,'Tree Plantation','Plant trees in Delhi park','Gardening','2 hours','Delhi','2025-09-05','2025-09-12','active','Environment'),
            (1,'River Cleanup','Help clean Yamuna river','Teamwork','5 hours','Delhi','2025-09-10','2025-09-20','active','Environment'),
            (2,'Dog Shelter Helper','Assist with feeding and cleaning','Animal care','3 hours','Mumbai','2025-09-01','2025-09-09','active','Animals')
        ]
    )

    # Finance (✅ includes opportunity_id now)
    cursor.executemany(
        "INSERT INTO ngo_finance (ngo_id, opportunity_id, type, amount, description, date) VALUES (%s,%s,%s,%s,%s,%s)",
        [
            (1,1,'collection',5000,'CSR donation from company','2025-09-01'),
            (1,1,'spending',1200,'Tools and gloves','2025-09-02'),
            (1,2,'collection',7000,'Local sponsorship','2025-09-05'),
            (1,2,'spending',2500,'Cleaning boats & nets','2025-09-06'),
            (2,3,'collection',3000,'Public donations','2025-09-01'),
            (2,3,'spending',1000,'Dog food','2025-09-02')
        ]
    )

    # Volunteer hours
    cursor.executemany(
        "INSERT INTO volunteer_hours (student_id, opportunity_id, hours) VALUES (%s,%s,%s)",
        [
            (1,1,5),(2,1,3),(3,2,4),(4,3,6)
        ]
    )

    conn.commit()
    conn.close()
    print("✅ Dummy data seeded successfully.")

if __name__ == "__main__":
    seed_data()
