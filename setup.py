#!/usr/bin/env python3
"""
QR Attendance System Setup Script
Initializes the database and creates default admin user
"""

import os
import sys
from database import init_db
from werkzeug.security import generate_password_hash
import sqlite3

def setup_database():
    """Initialize database and create default users"""
    print("🔧 Initializing database...")
    init_db()
    
    conn = sqlite3.connect('attendance.db')
    conn.row_factory = sqlite3.Row
    
    # Check if admin already exists
    existing_admin = conn.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()
    
    if not existing_admin:
        print("👤 Creating default admin user...")
        password_hash = generate_password_hash('admin123')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role) 
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin@system.com', password_hash, 'admin'))
        conn.commit()
        print("✅ Admin user created (username: admin, password: admin123)")
    else:
        print("ℹ️  Admin user already exists")
    
    conn.close()
    print("✅ Database setup complete!")

def main():
    """Main setup function"""
    print("🚀 QR Attendance System Setup")
    print("=" * 40)
    
    # Check if Python version is compatible
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        sys.exit(1)
    
    # Setup database
    setup_database()
    
    print("\n📋 Next Steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the application: python app.py")
    print("3. Open browser: http://localhost:5000")
    print("\n🔑 Default Login:")
    print("   Admin - username: admin, password: admin123")

if __name__ == '__main__':
    main()