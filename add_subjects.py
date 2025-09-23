import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

# Add sample subjects
subjects = [
    ('Artificial Intelligence', 'AI101', '1st Year', 'Section A', 3, 'Introduction to AI concepts', '1st Semester', 'Computer Science', 1),
    ('Machine Learning', 'ML201', '2nd Year', 'Section B', 4, 'ML algorithms and applications', '3rd Semester', 'Computer Science', 1),
    ('Data Structures', 'DS101', '1st Year', 'Section A', 3, 'Basic data structures', '1st Semester', 'Computer Science', 2),
    ('Database Management', 'DB301', '3rd Year', 'Section A', 4, 'Database design and management', '5th Semester', 'Computer Science', 2),
    ('Web Development', 'WD201', '2nd Year', 'Section B', 3, 'Frontend and backend development', '3rd Semester', 'Computer Science', 1)
]

for name, code, year, division, credits, desc, semester, dept, teacher_id in subjects:
    existing = cursor.execute('SELECT id FROM subjects WHERE code = ?', (code,)).fetchone()
    if not existing:
        cursor.execute('''
            INSERT INTO subjects (name, code, academic_year, division, credits, description, semester, department, teacher_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ''', (name, code, year, division, credits, desc, semester, dept, teacher_id))
        print(f'Added subject: {name}')

conn.commit()
conn.close()
print('Sample subjects added!')