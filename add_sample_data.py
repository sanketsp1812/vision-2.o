import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

# Sample students
students = [
    ('alice@example.com', 'Alice Johnson', 'STU101', 'password123'),
    ('bob@example.com', 'Bob Smith', 'STU102', 'password123'),
    ('charlie@example.com', 'Charlie Brown', 'STU103', 'password123'),
    ('diana@example.com', 'Diana Prince', 'STU104', 'password123'),
    ('eve@example.com', 'Eve Wilson', 'STU105', 'password123')
]

# Sample teachers
teachers = [
    ('prof.smith@example.com', 'Prof. John Smith', 'T101', 'Mathematics', 'password123'),
    ('dr.jones@example.com', 'Dr. Sarah Jones', 'T102', 'Physics', 'password123'),
    ('ms.davis@example.com', 'Ms. Emily Davis', 'T103', 'Chemistry', 'password123')
]

# Add students
for email, name, student_id, password in students:
    existing = cursor.execute('SELECT id FROM users WHERE username = ?', (email,)).fetchone()
    if not existing:
        password_hash = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
                      (email, email, password_hash, 'student'))
        user_id = cursor.lastrowid
        cursor.execute('INSERT INTO students (student_id, name, user_id) VALUES (?, ?, ?)',
                      (student_id, name, user_id))
        print(f'Added student: {email}')

# Add teachers
for email, name, teacher_id, subject, password in teachers:
    existing = cursor.execute('SELECT id FROM users WHERE username = ?', (email,)).fetchone()
    if not existing:
        password_hash = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
                      (email, email, password_hash, 'teacher'))
        user_id = cursor.lastrowid
        cursor.execute('INSERT INTO teachers (teacher_id, name, subject, user_id) VALUES (?, ?, ?, ?)',
                      (teacher_id, name, subject, user_id))
        print(f'Added teacher: {email}')

conn.commit()
conn.close()
print('Sample data added successfully!')