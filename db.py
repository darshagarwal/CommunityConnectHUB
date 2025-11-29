import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",         
    "password": "L@pt0pP@ssw0rd$2025!",             
    "database": "connecthub"
}

def get_connection():
    """Ensure DB exists and return a connection."""
    base_conf = {k: DB_CONFIG[k] for k in ("host","user","password")}
    conn = mysql.connector.connect(**base_conf)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    cur.close()
    conn.close()
    return mysql.connector.connect(**DB_CONFIG)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE,
        password VARCHAR(255),
        user_type ENUM('student','ngo')
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        name VARCHAR(150),
        grade INT,
        contact_email VARCHAR(150),
        interests TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ngos (
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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS opportunities (
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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_interests_opportunities (
        student_id INT,
        opportunity_id INT,
        date_expressed_interest DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (student_id, opportunity_id),
        FOREIGN KEY(student_id) REFERENCES students(student_id),
        FOREIGN KEY(opportunity_id) REFERENCES opportunities(opportunity_id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ngo_finance (
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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS volunteer_hours (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT,
        opportunity_id INT,
        hours INT,
        UNIQUE KEY ux_student_opportunity (student_id, opportunity_id),
        FOREIGN KEY(student_id) REFERENCES students(student_id),
        FOREIGN KEY(opportunity_id) REFERENCES opportunities(opportunity_id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("✅ Database and tables ready.")
