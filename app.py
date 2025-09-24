from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file, Response
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import qrcode
import io
import base64
from datetime import datetime
import os
import csv
from dotenv import load_dotenv
from database import init_db
from db_helper import execute_query, get_db_params

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 5242880))

# Initialize database
init_db()

def get_db_connection():
    database_url = os.getenv('DATABASE_URL', 'sqlite:///attendance.db')
    
    if database_url.startswith('postgresql'):
        import psycopg2
        from psycopg2.extras import RealDictCursor
        conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
        return conn
    else:
        import sqlite3
        conn = sqlite3.connect('attendance.db')
        conn.row_factory = sqlite3.Row
        return conn

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Access denied. Admin login required.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'teacher':
            flash('Access denied. Teacher login required.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'student':
            flash('Access denied. Student login required.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form.get('user_type', 'student')
        
        conn = get_db_connection()
        user = execute_query(conn, 'SELECT * FROM users WHERE username = ?', (username,), fetch_one=True)
        conn.close()
        
        if user:
            if check_password_hash(user['password_hash'], password):
                if user['role'] != user_type:
                    flash(f'Please select the correct user type. You are registered as a {user["role"]}')
                    return render_template('login.html')
                    
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                
                if user['role'] == 'admin':
                    return redirect(url_for('admin'))
                elif user['role'] == 'teacher':
                    return redirect(url_for('teacher_dashboard'))
                else:
                    return redirect(url_for('index'))
            else:
                flash('Invalid password')
        else:
            flash('Username not found')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        name = request.form['name']
        password = request.form['password']
        
        conn = get_db_connection()
        
        # Check if user already exists
        existing_user = conn.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email)).fetchone()
        
        if existing_user:
            flash('Username or email already exists')
        else:
            # Role-specific validation
            if role == 'student':
                student_id = request.form['student_id']
                existing_student = conn.execute('SELECT id FROM students WHERE student_id = ?', (student_id,)).fetchone()
                if existing_student:
                    flash('Student ID already exists')
                    conn.close()
                    return render_template('register.html')
            elif role == 'teacher':
                teacher_id = request.form['teacher_id']
                subject = request.form['subject']
                existing_teacher = conn.execute('SELECT id FROM teachers WHERE teacher_id = ?', (teacher_id,)).fetchone()
                if existing_teacher:
                    flash('Teacher ID already exists')
                    conn.close()
                    return render_template('register.html')
            
            # Create new user
            password_hash = generate_password_hash(password)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)',
                         (username, email, password_hash, role))
            user_id = cursor.lastrowid
            
            # Create role-specific record
            if role == 'student':
                cursor.execute('INSERT INTO students (student_id, name, user_id) VALUES (?, ?, ?)',
                             (student_id, name, user_id))
            elif role == 'teacher':
                cursor.execute('INSERT INTO teachers (teacher_id, name, subject, user_id) VALUES (?, ?, ?, ?)',
                             (teacher_id, name, subject, user_id))
            
            conn.commit()
            conn.close()
            
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        
        conn.close()
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    # Redirect based on role
    if session.get('role') == 'admin':
        return redirect(url_for('admin'))
    elif session.get('role') == 'teacher':
        return redirect(url_for('teacher_dashboard'))
    elif session.get('role') != 'student':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    student = execute_query(conn, '''
        SELECT s.name, s.student_id, u.email, s.division, s.academic_year 
        FROM students s 
        JOIN users u ON s.user_id = u.id 
        WHERE s.user_id = ?
    ''', (session['user_id'],), fetch_one=True)
    
    conn.close()
    
    if not student:
        return redirect(url_for('login'))
    
    return render_template('student_dashboard.html', 
                         student_name=student['name'],
                         student_id=student['student_id'],
                         student_email=student['email'],
                         student_division=student.get('division', 'Not Set'),
                         student_year=student.get('academic_year', 'Not Set'))

@app.route('/get_student_subjects')
@login_required
def get_student_subjects():
    if session.get('role') != 'student':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    conn = get_db_connection()
    # Get student's actual academic info
    student = execute_query(conn, 'SELECT * FROM students WHERE user_id = ?', (session['user_id'],), fetch_one=True)
    
    # Get all subjects (remove hardcoded filtering for now)
    subjects = execute_query(conn, 'SELECT * FROM subjects ORDER BY name', (), fetch_all=True)
    conn.close()
    
    subjects_data = []
    for subject in subjects:
        subjects_data.append({
            'id': subject['id'],
            'name': subject['name'],
            'code': subject['code'],
            'academic_year': subject['academic_year'],
            'division': subject['division'],
            'credits': subject['credits'],
            'semester': subject['semester']
        })
    
    return jsonify(subjects_data)

@app.route('/subjects')
@login_required
def subjects():
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    student = execute_query(conn, 'SELECT * FROM students WHERE user_id = ?', (session['user_id'],), fetch_one=True)
    # Get all subjects (remove hardcoded filtering)
    subjects = execute_query(conn, 'SELECT * FROM subjects ORDER BY name', (), fetch_all=True)
    conn.close()
    
    return render_template('subjects.html', student=student, subjects=subjects)

@app.route('/qr_scanner')
@app.route('/qr_scanner/<int:subject_id>')
@login_required
def qr_scanner(subject_id=None):
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    student = conn.execute('SELECT student_id FROM students WHERE user_id = ?', (session['user_id'],)).fetchone()
    
    subject = None
    if subject_id:
        subject = conn.execute('SELECT * FROM subjects WHERE id = ?', (subject_id,)).fetchone()
    
    conn.close()
    
    return render_template('qr_scanner.html', 
                         student_id=student['student_id'] if student else '001',
                         subject=subject)

@app.route('/teacher_dashboard')
@login_required
def teacher_dashboard():
    if session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    teacher = conn.execute('SELECT name FROM teachers WHERE user_id = ?', (session['user_id'],)).fetchone()
    
    # Get subjects created by this teacher
    subjects = conn.execute('''
        SELECT * FROM subjects WHERE teacher_id = ? ORDER BY created_at DESC
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    
    if not teacher:
        flash('Teacher profile not found.')
        return redirect(url_for('login'))
    
    return render_template('teacher_dashboard.html', teacher_name=teacher['name'], subjects=subjects)

@app.route('/admin')
@admin_required
def admin():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('admin.html', students=students)

@app.route('/generate_qr', methods=['POST'])
@login_required
def generate_qr():
    try:
        if session.get('role') not in ['admin', 'teacher']:
            return jsonify({'success': False, 'message': 'Unauthorized'})
        
        data = request.json
        if not data:
            return jsonify({'success': False, 'message': 'No data received'})
            
        subject = data.get('subject')
        class_start_time = data.get('class_start_time')
        class_end_time = data.get('class_end_time')
        expiry_seconds = int(data.get('expiry_seconds', 300))
        
        if not all([subject, class_start_time, class_end_time]):
            return jsonify({'success': False, 'message': 'All fields are required'})
        
        # Generate QR code with current timestamp
        qr_data = f"attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Calculate expiry time
        from datetime import timedelta
        expiry_time = datetime.now() + timedelta(seconds=expiry_seconds)
        
        # Store session in database
        conn = get_db_connection()
        execute_query(conn, '''
            INSERT INTO sessions (qr_data, subject, lecture_time, location, expiry_time, is_active) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (qr_data, subject, class_start_time, class_end_time, expiry_time.strftime('%Y-%m-%d %H:%M:%S'), True))
        conn.commit()
        conn.close()
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'qr_code': f'data:image/png;base64,{img_str}',
            'session_id': qr_data,
            'subject': subject,
            'class_start_time': class_start_time,
            'class_end_time': class_end_time,
            'expiry_seconds': expiry_seconds
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/mark_attendance', methods=['POST'])
@login_required
def mark_attendance():
    data = request.json
    student_id = data.get('student_id')
    session_id = data.get('session_id')
    
    conn = get_db_connection()
    
    # Check if student exists
    student = conn.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()
    if not student:
        conn.close()
        return jsonify({'success': False, 'message': 'Student not found'})
    
    # Check if session exists, is active, and not expired
    db_params = get_db_params()
    session_record = execute_query(conn, f'''
        SELECT id, subject, lecture_time, location, expiry_time 
        FROM sessions 
        WHERE qr_data = ? AND is_active = ? AND {db_params['now']} <= expiry_time
    ''', (session_id, True), fetch_one=True)
    
    if not session_record:
        conn.close()
        return jsonify({'success': False, 'message': 'QR code expired or invalid'})
    
    # Check if already marked
    existing = conn.execute('SELECT id FROM attendance WHERE student_id = ? AND session_id = ?', 
                          (student_id, session_record['id'])).fetchone()
    if existing:
        conn.close()
        return jsonify({'success': False, 'message': 'Already marked attendance'})
    
    # Mark attendance
    conn.execute('INSERT INTO attendance (student_id, session_id) VALUES (?, ?)',
                (student_id, session_record['id']))
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True, 
        'message': f'Attendance marked for {session_record["subject"]} at {session_record["lecture_time"]}'
    })

@app.route('/get_attendance')
@login_required
def get_attendance():
    if session.get('role') not in ['admin', 'teacher']:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    conn = get_db_connection()
    attendance_records = conn.execute('''
        SELECT s.name, s.student_id, a.marked_at, ses.qr_data
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        JOIN sessions ses ON a.session_id = ses.id
        ORDER BY a.marked_at DESC
    ''').fetchall()
    conn.close()
    
    attendance_data = []
    for record in attendance_records:
        attendance_data.append({
            'student_name': record['name'],
            'student_id': record['student_id'],
            'session_id': record['qr_data'],
            'timestamp': record['marked_at']
        })
    
    return jsonify(attendance_data)

@app.route('/get_students')
@login_required
def get_students():
    if session.get('role') not in ['admin', 'teacher']:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    conn = get_db_connection()
    students = conn.execute('SELECT student_id, name FROM students ORDER BY name').fetchall()
    conn.close()
    
    students_data = []
    for student in students:
        students_data.append({
            'student_id': student['student_id'],
            'name': student['name']
        })
    
    return jsonify(students_data)

@app.route('/activity')
@login_required
def activity():
    conn = get_db_connection()
    
    if session.get('role') == 'student':
        student = conn.execute('''
            SELECT s.student_id, s.name FROM students s 
            WHERE s.user_id = ?
        ''', (session['user_id'],)).fetchone()
        
        if not student:
            conn.close()
            return redirect(url_for('login'))
        
        # Get certificate-enabled activities with participation status
        activities = conn.execute('''
            SELECT a.*, t.name as teacher_name,
                   CASE WHEN ap.id IS NOT NULL THEN 1 ELSE 0 END as participated
            FROM activities a
            JOIN teachers t ON a.teacher_id = t.user_id
            LEFT JOIN activity_participants ap ON a.id = ap.activity_id AND ap.student_id = ?
            WHERE a.certificate_enabled = 1
            ORDER BY a.event_date ASC
        ''', (student['student_id'],)).fetchall()
        
        conn.close()
        return render_template('activity.html', student_name=student['name'], student_id=student['student_id'], activities=activities)
    
    elif session.get('role') in ['teacher', 'admin']:
        teacher = conn.execute('SELECT name FROM teachers WHERE user_id = ?', (session['user_id'],)).fetchone()
        conn.close()
        
        teacher_name = teacher['name'] if teacher else 'Teacher'
        return render_template('teacher_activity.html', teacher_name=teacher_name)
    
    conn.close()
    flash('Access denied.')
    return redirect(url_for('login'))

@app.route('/analytics')
@login_required
def analytics():
    if session.get('role') not in ['teacher', 'admin']:
        flash('Access denied.')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    total_students = conn.execute('SELECT COUNT(*) as count FROM students').fetchone()['count']
    
    recent_attendance = conn.execute('''
        SELECT COUNT(DISTINCT a.student_id) as present_count
        FROM attendance a
        WHERE a.marked_at >= date('now', '-30 days')
    ''').fetchone()
    
    conn.close()
    
    attendance_rate = (recent_attendance['present_count'] / total_students * 100) if total_students > 0 else 0
    
    return render_template('analytics.html', 
                         total_students=total_students,
                         attendance_rate=round(attendance_rate, 1))

@app.route('/delete_subject', methods=['POST'])
@login_required
def delete_subject():
    if session.get('role') != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.json
    subject_id = data.get('subject_id')
    
    if not subject_id:
        return jsonify({'success': False, 'message': 'Subject ID required'})
    
    conn = get_db_connection()
    try:
        # Verify the subject belongs to this teacher
        subject = conn.execute('SELECT id FROM subjects WHERE id = ? AND teacher_id = ?', (subject_id, session['user_id'])).fetchone()
        if not subject:
            conn.close()
            return jsonify({'success': False, 'message': 'Subject not found or access denied'})
        
        # Delete related data first (to maintain referential integrity)
        # Delete attendance records for sessions of this subject
        conn.execute('''
            DELETE FROM attendance WHERE session_id IN (
                SELECT s.id FROM sessions s 
                JOIN subjects sub ON s.subject = sub.name 
                WHERE sub.id = ?
            )
        ''', (subject_id,))
        
        # Delete sessions for this subject
        conn.execute('''
            DELETE FROM sessions WHERE subject IN (
                SELECT name FROM subjects WHERE id = ?
            )
        ''', (subject_id,))
        
        # Delete results for this subject
        conn.execute('DELETE FROM results WHERE subject_id = ?', (subject_id,))
        
        # Finally delete the subject
        conn.execute('DELETE FROM subjects WHERE id = ? AND teacher_id = ?', (subject_id, session['user_id']))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Subject deleted successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': 'Failed to delete subject'})

@app.route('/create_subject', methods=['POST'])
@login_required
def create_subject():
    if session.get('role') != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.json
    subject_name = data.get('subjectName')
    academic_year = data.get('academicYear')
    division = data.get('division')
    subject_code = data.get('subjectCode', '')
    credits = data.get('credits', 3)
    description = data.get('description', '')
    semester = data.get('semester', '')
    department = data.get('department', '')
    
    if not all([subject_name, academic_year, division]):
        return jsonify({'success': False, 'message': 'Required fields missing'})
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO subjects (name, code, academic_year, division, credits, description, semester, department, teacher_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ''', (subject_name, subject_code, academic_year, division, credits, description, semester, department, session['user_id']))
        subject_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Subject created successfully', 'subject_id': subject_id})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': 'Database error'})

@app.route('/library')
@login_required
def library():
    conn = get_db_connection()
    
    if session.get('role') == 'student':
        student = conn.execute('''
            SELECT s.name FROM students s 
            WHERE s.user_id = ?
        ''', (session['user_id'],)).fetchone()
        
        conn.close()
        if not student:
            return redirect(url_for('login'))
        return render_template('library.html', student_name=student['name'])
    
    elif session.get('role') in ['teacher', 'admin']:
        teacher = conn.execute('SELECT name FROM teachers WHERE user_id = ?', (session['user_id'],)).fetchone()
        conn.close()
        
        teacher_name = teacher['name'] if teacher else 'Teacher'
        return render_template('teacher_library.html', teacher_name=teacher_name)
    
    conn.close()
    flash('Access denied.')
    return redirect(url_for('login'))

@app.route('/submit_leave', methods=['POST'])
@login_required
def submit_leave():
    if session.get('role') != 'student':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    leave_type = request.form.get('leaveType')
    start_date = request.form.get('startDate')
    end_date = request.form.get('endDate')
    reason = request.form.get('reason')
    
    print(f"Received data: {leave_type}, {start_date}, {end_date}, {reason}")
    
    if not all([leave_type, start_date, end_date, reason]):
        return jsonify({'success': False, 'message': 'All fields are required'})
    
    # Handle file upload
    attachment_path = None
    try:
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename:
                upload_dir = 'uploads/leave_documents'
                os.makedirs(upload_dir, exist_ok=True)
                
                filename = secure_filename(f"{session['user_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                attachment_path = os.path.join(upload_dir, filename)
                file.save(attachment_path)
    except Exception as e:
        print(f"File upload error: {str(e)}")
        return jsonify({'success': False, 'message': f'File upload error: {str(e)}'})
    
    conn = get_db_connection()
    student = conn.execute('SELECT student_id, name FROM students WHERE user_id = ?', (session['user_id'],)).fetchone()
    
    if not student:
        conn.close()
        return jsonify({'success': False, 'message': 'Student not found'})
    
    try:
        conn.execute('''
            INSERT INTO leave_applications (student_id, student_name, leave_type, start_date, end_date, reason, attachment_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (student['student_id'], student['name'], leave_type, start_date, end_date, reason, attachment_path))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Leave application submitted successfully'})
    except Exception as e:
        conn.close()
        print(f"Database error: {str(e)}")
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'})

@app.route('/get_leave_applications')
@login_required
def get_leave_applications():
    if session.get('role') not in ['teacher', 'admin']:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    conn = get_db_connection()
    applications = conn.execute('''
        SELECT * FROM leave_applications 
        ORDER BY applied_at DESC
    ''').fetchall()
    conn.close()
    
    apps_data = []
    for app in applications:
        apps_data.append({
            'id': app['id'],
            'student_id': app['student_id'],
            'student_name': app['student_name'],
            'leave_type': app['leave_type'],
            'start_date': app['start_date'],
            'end_date': app['end_date'],
            'reason': app['reason'],
            'status': app['status'],
            'applied_at': app['applied_at'],
            'attachment_path': app.get('attachment_path')
        })
    
    return jsonify(apps_data)

@app.route('/update_leave_status', methods=['POST'])
@login_required
def update_leave_status():
    if session.get('role') not in ['teacher', 'admin']:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.json
    app_id = data.get('id')
    status = data.get('status')
    
    if not all([app_id, status]) or status not in ['approved', 'rejected']:
        return jsonify({'success': False, 'message': 'Invalid data'})
    
    conn = get_db_connection()
    try:
        conn.execute('''
            UPDATE leave_applications 
            SET status = ?, reviewed_at = datetime('now'), reviewed_by = ?
            WHERE id = ?
        ''', (status, session['user_id'], app_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Application {status} successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': 'Failed to update status'})

@app.route('/create_activity', methods=['POST'])
@login_required
def create_activity():
    if session.get('role') not in ['teacher', 'admin']:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.json
    title = data.get('title')
    description = data.get('description')
    activity_type = data.get('activity_type')
    event_date = data.get('event_date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    location = data.get('location')
    max_participants = data.get('max_participants', 100)
    requirements = data.get('requirements', '')
    organizer = data.get('organizer')
    certificate_enabled = data.get('certificate_enabled', False)
    
    if not all([title, description, activity_type, event_date, start_time, end_time, location, organizer]):
        return jsonify({'success': False, 'message': 'All required fields must be filled'})
    
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO activities (title, description, activity_type, event_date, start_time, end_time, location, max_participants, requirements, organizer, teacher_id, certificate_enabled)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, activity_type, event_date, start_time, end_time, location, max_participants, requirements, organizer, session['user_id'], certificate_enabled))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Activity created successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': 'Failed to create activity'})

@app.route('/get_activities')
@login_required
def get_activities():
    conn = get_db_connection()
    activities = conn.execute('''
        SELECT a.*, t.name as teacher_name
        FROM activities a
        JOIN teachers t ON a.teacher_id = t.user_id
        ORDER BY a.event_date ASC
    ''').fetchall()
    conn.close()
    
    activities_data = []
    for activity in activities:
        activities_data.append({
            'id': activity['id'],
            'title': activity['title'],
            'description': activity['description'],
            'activity_type': activity['activity_type'],
            'event_date': activity['event_date'],
            'start_time': activity['start_time'],
            'end_time': activity['end_time'],
            'location': activity['location'],
            'max_participants': activity['max_participants'],
            'requirements': activity['requirements'],
            'organizer': activity['organizer'],
            'teacher_name': activity['teacher_name'],
            'created_at': activity['created_at']
        })
    
    return jsonify(activities_data)

@app.route('/download_attachment/<int:app_id>')
@login_required
def download_attachment(app_id):
    if session.get('role') not in ['teacher', 'admin']:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    conn = get_db_connection()
    app = conn.execute('SELECT attachment_path FROM leave_applications WHERE id = ?', (app_id,)).fetchone()
    conn.close()
    
    if not app or not app['attachment_path']:
        return jsonify({'success': False, 'message': 'File not found'})
    
    if os.path.exists(app['attachment_path']):
        return send_file(app['attachment_path'], as_attachment=True)
    else:
        return jsonify({'success': False, 'message': 'File not found on server'})

@app.route('/qr_display/<session_id>')
@login_required
def qr_display(session_id):
    if session.get('role') not in ['admin', 'teacher']:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    qr_session = conn.execute('''
        SELECT * FROM sessions WHERE qr_data = ? AND is_active = 1
    ''', (session_id,)).fetchone()
    conn.close()
    
    if not qr_session:
        flash('QR session not found or expired')
        return redirect(url_for('teacher_dashboard'))
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(session_id)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    # Calculate remaining time
    from datetime import datetime
    expiry_time = datetime.strptime(qr_session['expiry_time'], '%Y-%m-%d %H:%M:%S')
    remaining_seconds = max(0, int((expiry_time - datetime.now()).total_seconds()))
    
    return render_template('qr_display.html',
                         subject=qr_session['subject'],
                         qr_image=img_str,
                         class_start_time=datetime.strptime(qr_session['lecture_time'], '%Y-%m-%dT%H:%M'),
                         class_end_time=datetime.strptime(qr_session['location'], '%Y-%m-%dT%H:%M'),
                         expiry_seconds=remaining_seconds)

@app.route('/get_subject_attendance/<int:subject_id>')
@login_required
def get_subject_attendance(subject_id):
    if session.get('role') != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    conn = get_db_connection()
    attendance_records = conn.execute('''
        SELECT s.name, s.student_id, a.marked_at, ses.subject
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        JOIN sessions ses ON a.session_id = ses.id
        JOIN subjects sub ON ses.subject = sub.name
        WHERE sub.id = ? AND sub.teacher_id = ?
        ORDER BY a.marked_at DESC
    ''', (subject_id, session['user_id'])).fetchall()
    conn.close()
    
    attendance_data = []
    for record in attendance_records:
        attendance_data.append({
            'student_name': record['name'],
            'student_id': record['student_id'],
            'subject': record['subject'],
            'timestamp': record['marked_at']
        })
    
    return jsonify(attendance_data)

@app.route('/download_attendance_csv/<int:subject_id>')
@login_required
def download_attendance_csv(subject_id):
    if session.get('role') != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    conn = get_db_connection()
    subject = conn.execute('SELECT name FROM subjects WHERE id = ? AND teacher_id = ?', (subject_id, session['user_id'])).fetchone()
    if not subject:
        conn.close()
        return jsonify({'success': False, 'message': 'Subject not found'})
    
    attendance_records = conn.execute('''
        SELECT s.name, s.student_id, a.marked_at, ses.subject
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        JOIN sessions ses ON a.session_id = ses.id
        JOIN subjects sub ON ses.subject = sub.name
        WHERE sub.id = ? AND sub.teacher_id = ?
        ORDER BY a.marked_at DESC
    ''', (subject_id, session['user_id'])).fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Student Name', 'Student ID', 'Subject', 'Attendance Date'])
    
    for record in attendance_records:
        writer.writerow([record['name'], record['student_id'], record['subject'], record['marked_at']])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={subject["name"]}_attendance.csv'}
    )

@app.route('/get_subject_leave_applications/<int:subject_id>')
@login_required
def get_subject_leave_applications(subject_id):
    if session.get('role') != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    conn = get_db_connection()
    subject = conn.execute('SELECT name FROM subjects WHERE id = ? AND teacher_id = ?', (subject_id, session['user_id'])).fetchone()
    if not subject:
        conn.close()
        return jsonify({'success': False, 'message': 'Subject not found'})
    
    applications = conn.execute('''
        SELECT * FROM leave_applications 
        ORDER BY applied_at DESC
    ''').fetchall()
    conn.close()
    
    apps_data = []
    for app in applications:
        apps_data.append({
            'id': app['id'],
            'student_id': app['student_id'],
            'student_name': app['student_name'],
            'leave_type': app['leave_type'],
            'start_date': app['start_date'],
            'end_date': app['end_date'],
            'reason': app['reason'],
            'status': app['status'],
            'applied_at': app['applied_at'],
            'attachment_path': app.get('attachment_path')
        })
    
    return jsonify(apps_data)

@app.route('/enter_result', methods=['POST'])
@login_required
def enter_result():
    if session.get('role') != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    data = request.json
    student_id = data.get('student_id')
    subject_id = data.get('subject_id')
    exam_type = data.get('exam_type')
    marks_obtained = data.get('marks_obtained')
    max_marks = data.get('max_marks')
    remarks = data.get('remarks', '')
    
    if not all([student_id, subject_id, exam_type, marks_obtained, max_marks]):
        return jsonify({'success': False, 'message': 'All fields are required'})
    
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO results (student_id, subject_id, exam_type, marks_obtained, max_marks, remarks, teacher_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ''', (student_id, subject_id, exam_type, marks_obtained, max_marks, remarks, session['user_id']))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Result saved successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': 'Failed to save result'})

@app.route('/get_students_subjects')
@login_required
def get_students_subjects():
    if session.get('role') != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    conn = get_db_connection()
    students = conn.execute('SELECT student_id, name FROM students ORDER BY name').fetchall()
    subjects = conn.execute('SELECT id, name, academic_year, division FROM subjects WHERE teacher_id = ? ORDER BY name', (session['user_id'],)).fetchall()
    conn.close()
    
    return jsonify({
        'students': [{'id': s['student_id'], 'name': s['name']} for s in students],
        'subjects': [{'id': s['id'], 'name': s['name'], 'year': s['academic_year'], 'division': s['division']} for s in subjects]
    })

@app.route('/upload_results_csv', methods=['POST'])
@login_required
def upload_results_csv():
    if session.get('role') != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.csv'):
        return jsonify({'success': False, 'message': 'Please upload a CSV file'})
    
    try:
        content = file.read().decode('utf-8')
        lines = content.strip().split('\n')
        
        if len(lines) < 2:
            return jsonify({'success': False, 'message': 'CSV must have header and data rows'})
        
        conn = get_db_connection()
        success_count = 0
        error_count = 0
        
        for line in lines[1:]:  # Skip header
            try:
                parts = [p.strip() for p in line.split(',')]
                if len(parts) >= 6:
                    student_id, name, subject_id, exam_type, marks_obtained, max_marks = parts[:6]
                    remarks = parts[6] if len(parts) > 6 else ''
                    
                    conn.execute('''
                        INSERT INTO results (student_id, subject_id, exam_type, marks_obtained, max_marks, remarks, teacher_id, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
                    ''', (student_id, int(subject_id), exam_type, float(marks_obtained), float(max_marks), remarks, session['user_id']))
                    success_count += 1
            except:
                error_count += 1
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': f'Uploaded {success_count} results successfully. {error_count} errors.'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to process CSV file'})

@app.route('/join_activity/<int:activity_id>', methods=['POST'])
@login_required
def join_activity(activity_id):
    if session.get('role') != 'student':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    conn = get_db_connection()
    student = conn.execute('SELECT student_id, name FROM students WHERE user_id = ?', (session['user_id'],)).fetchone()
    
    if not student:
        conn.close()
        return jsonify({'success': False, 'message': 'Student not found'})
    
    # Check if already joined
    existing = conn.execute('SELECT id FROM activity_participants WHERE activity_id = ? AND student_id = ?', (activity_id, student['student_id'])).fetchone()
    if existing:
        conn.close()
        return jsonify({'success': False, 'message': 'Already joined this activity'})
    
    try:
        conn.execute('INSERT INTO activity_participants (activity_id, student_id, student_name) VALUES (?, ?, ?)', (activity_id, student['student_id'], student['name']))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Successfully joined activity'})
    except:
        conn.close()
        return jsonify({'success': False, 'message': 'Failed to join activity'})

@app.route('/download_certificate/<int:activity_id>')
@login_required
def download_certificate(activity_id):
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    student = conn.execute('SELECT student_id, name FROM students WHERE user_id = ?', (session['user_id'],)).fetchone()
    
    if not student:
        conn.close()
        return redirect(url_for('login'))
    
    # Check participation and certificate eligibility
    activity = conn.execute('''
        SELECT a.*, ap.participated_at 
        FROM activities a 
        JOIN activity_participants ap ON a.id = ap.activity_id 
        WHERE a.id = ? AND ap.student_id = ? AND a.certificate_enabled = 1
    ''', (activity_id, student['student_id'])).fetchone()
    
    conn.close()
    
    if not activity:
        flash('Certificate not available')
        return redirect(url_for('index'))
    
    return render_template('certificate.html', 
                         student_name=student['name'],
                         student_id=student['student_id'],
                         activity=activity)

if __name__ == '__main__':
    app.run(debug=True)