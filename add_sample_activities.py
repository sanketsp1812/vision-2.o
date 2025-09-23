import sqlite3
from datetime import datetime, timedelta

def add_sample_activities():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    # Get teacher user ID
    teacher = cursor.execute('SELECT id FROM users WHERE role = "teacher" LIMIT 1').fetchone()
    if not teacher:
        print("No teacher found in database")
        return
    
    teacher_id = teacher[0]
    
    # Sample activities
    activities = [
        {
            'title': 'National Coding Championship',
            'description': 'Compete in algorithmic challenges and win amazing prizes. Test your programming skills against the best students.',
            'activity_type': 'competition',
            'event_date': '2024-12-15',
            'start_time': '10:00',
            'end_time': '18:00',
            'location': 'Main Auditorium',
            'max_participants': 250,
            'requirements': 'Programming Skills, Problem Solving',
            'organizer': 'Computer Science Department',
            'teacher_id': teacher_id
        },
        {
            'title': 'AI Workshop by Google',
            'description': 'Learn AI fundamentals from Google engineers. Hands-on experience with machine learning tools.',
            'activity_type': 'workshop',
            'event_date': '2024-12-20',
            'start_time': '14:00',
            'end_time': '17:00',
            'location': 'Tech Lab A',
            'max_participants': 100,
            'requirements': 'Basic Python knowledge',
            'organizer': 'Tech Innovation Club',
            'teacher_id': teacher_id
        },
        {
            'title': 'Cultural Fest Opening Ceremony',
            'description': 'Grand opening of the annual cultural festival with performances, music, and dance.',
            'activity_type': 'cultural',
            'event_date': '2024-12-18',
            'start_time': '17:00',
            'end_time': '20:00',
            'location': 'Open Grounds',
            'max_participants': 500,
            'requirements': 'Open to All',
            'organizer': 'Cultural Committee',
            'teacher_id': teacher_id
        },
        {
            'title': 'Basketball Tournament Finals',
            'description': 'Inter-department basketball championship finals. Come support your department team!',
            'activity_type': 'sports',
            'event_date': '2024-12-22',
            'start_time': '16:00',
            'end_time': '19:00',
            'location': 'Sports Complex',
            'max_participants': 96,
            'requirements': 'Team Registration Required',
            'organizer': 'Sports Committee',
            'teacher_id': teacher_id
        },
        {
            'title': 'Entrepreneurship Summit',
            'description': 'Learn from successful entrepreneurs and startup founders. Network with industry leaders.',
            'activity_type': 'seminar',
            'event_date': '2024-12-25',
            'start_time': '13:00',
            'end_time': '18:00',
            'location': 'Business Center',
            'max_participants': 200,
            'requirements': 'Business Interest',
            'organizer': 'E-Cell',
            'teacher_id': teacher_id
        }
    ]
    
    # Insert activities
    for activity in activities:
        cursor.execute('''
            INSERT INTO activities (title, description, activity_type, event_date, start_time, end_time, location, max_participants, requirements, organizer, teacher_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            activity['title'],
            activity['description'],
            activity['activity_type'],
            activity['event_date'],
            activity['start_time'],
            activity['end_time'],
            activity['location'],
            activity['max_participants'],
            activity['requirements'],
            activity['organizer'],
            activity['teacher_id']
        ))
    
    conn.commit()
    conn.close()
    print(f"Added {len(activities)} sample activities successfully!")

if __name__ == '__main__':
    add_sample_activities()