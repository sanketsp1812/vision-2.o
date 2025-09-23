import sqlite3
from werkzeug.security import check_password_hash

conn = sqlite3.connect('attendance.db')
conn.row_factory = sqlite3.Row

# Test student1@gmail.com
user = conn.execute('SELECT password_hash FROM users WHERE username = ?', ('student1@gmail.com',)).fetchone()
if user:
    print('Password check for student1@gmail.com with password "student123":', check_password_hash(user['password_hash'], 'student123'))
else:
    print('User student1@gmail.com not found')

# Test admin
user = conn.execute('SELECT password_hash FROM users WHERE username = ?', ('admin',)).fetchone()
if user:
    print('Password check for admin with password "admin123":', check_password_hash(user['password_hash'], 'admin123'))
else:
    print('User admin not found')

conn.close()