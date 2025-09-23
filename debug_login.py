import sqlite3
from werkzeug.security import check_password_hash

def test_login(username, password, user_type):
    conn = sqlite3.connect('attendance.db')
    conn.row_factory = sqlite3.Row
    
    print(f"Testing login for: {username}, password: {password}, user_type: {user_type}")
    
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    
    if user:
        print(f"User found: {user['username']}, role: {user['role']}")
        password_check = check_password_hash(user['password_hash'], password)
        print(f"Password check: {password_check}")
        
        if password_check:
            if user['role'] != user_type:
                print(f"Role mismatch: user role is {user['role']}, requested {user_type}")
                return False
            else:
                print("Login successful!")
                return True
        else:
            print("Password incorrect")
            return False
    else:
        print("User not found")
        return False
    
    conn.close()

# Test cases
print("=== Testing login scenarios ===")
test_login('student1@gmail.com', 'student123', 'student')
print()
test_login('teacher1@gmail.com', 'teacher123', 'teacher')
print()
test_login('admin', 'admin123', 'admin')