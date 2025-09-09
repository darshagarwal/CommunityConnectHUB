import mysql.connector

# ================= DB CONFIG ================= #
DB_CONFIG = {
    "host": "localhost",
    "user": "root",             # 🔑 change this
    "password": "your_password",# 🔑 change this
    "database": "community_connect"
}

def get_connection():
    """Create and return a database connection."""
    return mysql.connector.connect(**DB_CONFIG)

# ================= SEEDING LOGIC ================= #

def seed_database():
    """Reset all tables and insert dummy data."""
    conn = get_connection()
    cursor = conn.cursor()

    # Drop tables in order
    drop_order = [
        "volunteer_hours",
        "ngo_finance",
        "student_interests_opportunities",
        "opportunities",
        "students",
        "ngos",
        "users"
    ]
    for table in drop_order:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    # Create tables
    cursor.execute("""
    CREATE TABLE users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE,
        password VARCHAR(255),
        user_type ENUM('student','ngo')
    )
    """)

    cursor.execute("""
    CREATE TABLE students (
        student_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        name VARCHAR(150),
        grade INT,
        contact_email VARCHAR(150),
        interests TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE ngos (
        ngo_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        name VARCHAR(150),
        mission_statement TEXT,
        address VARCHAR(255),
        contact_person VARCHAR(100),
        contact_email VARCHAR(150),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE opportunities (
        opportunity_id INT AUTO_INCREMENT PRIMARY KEY,
        ngo_id INT,
        title VARCHAR(200),
        description TEXT,
        required_skills TEXT,
        time_commitment VARCHAR(100),
        location VARCHAR(100),
        start_date DATE,
        end_date DATE,
        status ENUM('active','filled','archived','ended') DEFAULT 'active',
        category VARCHAR(50),
        FOREIGN KEY(ngo_id) REFERENCES ngos(ngo_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE student_interests_opportunities (
        student_id INT,
        opportunity_id INT,
        date_expressed_interest DATETIME,
        PRIMARY KEY (student_id, opportunity_id),
        FOREIGN KEY(student_id) REFERENCES students(student_id),
        FOREIGN KEY(opportunity_id) REFERENCES opportunities(opportunity_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE ngo_finance (
        finance_id INT AUTO_INCREMENT PRIMARY KEY,
        ngo_id INT,
        opportunity_id INT,
        type ENUM('spending','collection'),
        amount DECIMAL(12,2),
        description TEXT,
        date DATE,
        FOREIGN KEY(ngo_id) REFERENCES ngos(ngo_id),
        FOREIGN KEY(opportunity_id) REFERENCES opportunities(opportunity_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE volunteer_hours (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT,
        opportunity_id INT,
        hours INT,
        UNIQUE KEY ux_student_opportunity (student_id, opportunity_id),
        FOREIGN KEY(student_id) REFERENCES students(student_id),
        FOREIGN KEY(opportunity_id) REFERENCES opportunities(opportunity_id)
    )
    """)

    # Insert dummy data
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

    cursor.executemany(
        "INSERT INTO ngos (user_id, name, mission_statement, address, contact_person, contact_email) VALUES (%s,%s,%s,%s,%s,%s)",
        [
            (9,'Green Earth','Protecting environment and organizing cleanups','Delhi','Meena Gupta','greenearth@example.com'),
            (10,'Animal Care','Helping street animals find homes','Mumbai','Rohit Sen','animalcare@example.com'),
            (11,'EduHelp','Tutoring underprivileged kids','Kolkata','Priya Nair','eduhelp@example.com')
        ]
    )

    cursor.executemany(
        "INSERT INTO opportunities (ngo_id, title, description, required_skills, time_commitment, location, start_date, end_date, status, category) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        [
            (1,'Tree Plantation','Plant trees in Delhi park','Gardening','2 hours','Delhi','2025-09-05','2025-09-12','active','Environment'),
            (1,'River Cleanup','Help clean Yamuna river','Teamwork','5 hours','Delhi','2025-09-10','2025-09-20','active','Environment'),
            (2,'Dog Shelter Helper','Assist with feeding and cleaning','Animal care','3 hours','Mumbai','2025-09-01','2025-09-09','active','Animals')
        ]
    )

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

    cursor.executemany(
        "INSERT INTO volunteer_hours (student_id, opportunity_id, hours) VALUES (%s,%s,%s)",
        [
            (1,1,5),(2,1,3),(3,2,4),(4,3,6)
        ]
    )

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database seeded with dummy data.")

if __name__ == "__main__":
    seed_database()
