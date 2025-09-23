import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    # Check if missing columns exist in sessions table, add if missing
    try:
        cursor.execute("ALTER TABLE sessions ADD COLUMN subject TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute("ALTER TABLE sessions ADD COLUMN lecture_time TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute("ALTER TABLE sessions ADD COLUMN location TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute("ALTER TABLE sessions ADD COLUMN expiry_time TIMESTAMP")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Users table for authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Teachers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            subject TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Attendance sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            qr_data TEXT UNIQUE NOT NULL,
            subject TEXT,
            lecture_time TEXT,
            location TEXT,
            expiry_time TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Attendance records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            session_id INTEGER NOT NULL,
            marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        )
    ''')
    
    # Subjects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT,
            academic_year TEXT NOT NULL,
            division TEXT NOT NULL,
            credits INTEGER DEFAULT 3,
            description TEXT,
            semester TEXT,
            department TEXT,
            teacher_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES users (id)
        )
    ''')
    
    # Leave applications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leave_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            student_name TEXT NOT NULL,
            leave_type TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            reason TEXT NOT NULL,
            attachment_path TEXT,
            status TEXT DEFAULT 'pending',
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reviewed_at TIMESTAMP,
            reviewed_by INTEGER,
            FOREIGN KEY (reviewed_by) REFERENCES users (id)
        )
    ''')
    
    # Activities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            activity_type TEXT NOT NULL,
            event_date DATE NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            location TEXT NOT NULL,
            max_participants INTEGER,
            requirements TEXT,
            organizer TEXT NOT NULL,
            teacher_id INTEGER NOT NULL,
            certificate_enabled BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES users (id)
        )
    ''')
    
    # Add certificate_enabled column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE activities ADD COLUMN certificate_enabled BOOLEAN DEFAULT 0")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Activity participants table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_id INTEGER NOT NULL,
            student_id TEXT NOT NULL,
            student_name TEXT NOT NULL,
            participated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (activity_id) REFERENCES activities (id)
        )
    ''')
    
    # Results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject_id INTEGER NOT NULL,
            exam_type TEXT NOT NULL,
            marks_obtained REAL NOT NULL,
            max_marks REAL NOT NULL,
            remarks TEXT,
            teacher_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (subject_id) REFERENCES subjects (id),
            FOREIGN KEY (teacher_id) REFERENCES users (id)
        )
    ''')
    
    # Create default admin user
    admin_hash = generate_password_hash('admin123')
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, email, password_hash, role)
        VALUES (?, ?, ?, ?)
    ''', ('admin', 'admin@example.com', admin_hash, 'admin'))
    
    # Create default teacher user
    teacher_hash = generate_password_hash('teacher123')
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, email, password_hash, role)
        VALUES (?, ?, ?, ?)
    ''', ('teacher', 'teacher@example.com', teacher_hash, 'teacher'))
    
    # Get teacher user ID and create teacher record
    teacher_user = cursor.execute('SELECT id FROM users WHERE username = ?', ('teacher',)).fetchone()
    if teacher_user:
        cursor.execute('''
            INSERT OR IGNORE INTO teachers (teacher_id, name, subject, user_id)
            VALUES (?, ?, ?, ?)
        ''', ('T001', 'Sanket Patil', 'Computer Science', teacher_user[0]))
    
    # Add sample students
    sample_students = [
        ('student1@gmail.com', 'student123', '001', 'John Doe'),
        ('student2@gmail.com', 'student123', '002', 'Jane Smith'),
        ('student3@gmail.com', 'student123', '003', 'Mike Johnson'),
        ('sanketpatil@gmail.com', 'student123', '5345', 'Sanket Patil')
    ]
    
    for email, password, student_id, name in sample_students:
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        ''', (email, email, password_hash, 'student'))
        
        user_id = cursor.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if user_id:
            cursor.execute('''
                INSERT OR IGNORE INTO students (student_id, name, user_id)
                VALUES (?, ?, ?)
            ''', (student_id, name, user_id[0]))
    
    # Add sample teachers
    sample_teachers = [
        ('teacher1@gmail.com', 'teacher123', 'T002', 'Dr. Smith', 'Mathematics'),
        ('teacher2@gmail.com', 'teacher123', 'T003', 'Prof. Johnson', 'Physics')
    ]
    
    for email, password, teacher_id, name, subject in sample_teachers:
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        ''', (email, email, password_hash, 'teacher'))
        
        user_id = cursor.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if user_id:
            cursor.execute('''
                INSERT OR IGNORE INTO teachers (teacher_id, name, subject, user_id)
                VALUES (?, ?, ?, ?)
            ''', (teacher_id, name, subject, user_id[0]))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")