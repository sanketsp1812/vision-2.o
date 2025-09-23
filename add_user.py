import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('attendance.db')
conn.row_factory = sqlite3.Row

# Add jayupatil@example.com as student
username = 'jayupatil@example.com'
password = 'sanyu'
role = 'student'
name = 'Jayu Patil'
student_id = 'STU004'

# Check if user already exists
existing = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
if existing:
    print(f'User {username} already exists')
else:
    # Create user
    password_hash = generate_password_hash(password)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
                   (username, username, password_hash, role))
    user_id = cursor.lastrowid
    
    # Create student record
    cursor.execute('INSERT INTO students (student_id, name, user_id) VALUES (?, ?, ?)',
                   (student_id, name, user_id))
    
    conn.commit()
    print(f'User {username} created successfully with password: {password}')

conn.close()