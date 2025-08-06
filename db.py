import mysql.connector
from mysql.connector import errorcode

DB_NAME = "connecthub"

TABLES = {}

TABLES['users'] = (
    """CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        user_type ENUM('student', 'ngo') NOT NULL
    )"""
)

TABLES['students'] = (
    """CREATE TABLE IF NOT EXISTS students (
        student_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        name VARCHAR(255),
        grade INT,
        contact_email VARCHAR(255),
        contact_phone VARCHAR(20),
        interests TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )"""
)

TABLES['ngos'] = (
    """CREATE TABLE IF NOT EXISTS ngos (
        ngo_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        name VARCHAR(255),
        mission_statement TEXT,
        address VARCHAR(255),
        contact_person VARCHAR(255),
        contact_email VARCHAR(255),
        website VARCHAR(255),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )"""
)

TABLES['opportunities'] = (
    """CREATE TABLE IF NOT EXISTS opportunities (
        opportunity_id INT AUTO_INCREMENT PRIMARY KEY,
        ngo_id INT,
        title VARCHAR(255),
        description TEXT,
        required_skills TEXT,
        time_commitment VARCHAR(255),
        location VARCHAR(255),
        start_date DATE,
        end_date DATE,
        status ENUM('active', 'filled', 'archived') DEFAULT 'active',
        category VARCHAR(100),
        FOREIGN KEY (ngo_id) REFERENCES ngos(ngo_id)
    )"""
)

TABLES['student_interests_opportunities'] = (
    """CREATE TABLE IF NOT EXISTS student_interests_opportunities (
        student_id INT,
        opportunity_id INT,
        date_expressed_interest DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (student_id, opportunity_id),
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (opportunity_id) REFERENCES opportunities(opportunity_id)
    )"""
)




def get_connection():
    # Update these values
    config = {
        'host':"localhost",
        'user':"root",
        'password':"L@pt0pP@ssw0rd$2025!",
    }

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.database = DB_NAME

        # Create tables
        for table_name in TABLES:
            cursor.execute(TABLES[table_name])

        # Insert sample data if tables are empty
        insert_sample_data(conn, cursor)

        return conn

    except mysql.connector.Error as err:
        print("❌ Database error:", err)
        return None


def insert_sample_data(conn, cursor):
    # Check if there are any users
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Sample NGO user
        cursor.execute("INSERT INTO users (username, password, user_type) VALUES ('ngo_demo', 'demo123', 'ngo')")
        ngo_user_id = cursor.lastrowid
        cursor.execute("""INSERT INTO ngos (user_id, name, mission_statement, address, contact_person, contact_email, website)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                       (ngo_user_id, "Helping Hands", "Helping poor children", "123 Main St", "Alice", "alice@ngo.org", "http://helpinghands.org"))

        # Sample Student user
        cursor.execute("INSERT INTO users (username, password, user_type) VALUES ('student_demo', 'demo123', 'student')")
        student_user_id = cursor.lastrowid
        cursor.execute("""INSERT INTO students (user_id, name, grade, contact_email, contact_phone, interests)
                          VALUES (%s, %s, %s, %s, %s, %s)""",
                       (student_user_id, "Bob", 11, "bob@student.com", "1234567890", "education, animal welfare"))

        # Sample opportunity
        cursor.execute("SELECT ngo_id FROM ngos WHERE user_id = %s", (ngo_user_id,))
        ngo_id = cursor.fetchone()[0]

        cursor.execute("""INSERT INTO opportunities 
            (ngo_id, title, description, required_skills, time_commitment, location, start_date, end_date, category)
            VALUES (%s, %s, %s, %s, %s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 30 DAY), %s)""",
            (ngo_id, "Tutor Kids", "Teach basic English to underprivileged children", "good with kids", "2 hours/week", "Delhi", "Education"))

        conn.commit()
        print("✅ Sample data inserted.")

