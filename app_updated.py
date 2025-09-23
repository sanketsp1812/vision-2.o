# Add these imports to the top of your app.py file
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file, Response

# Add these routes to your existing app.py file (after the existing routes)

@app.route('/get_subject_attendance/<int:subject_id>')
@login_required
def get_subject_attendance(subject_id):
    if session.get('role') != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    date_filter = request.args.get('date')
    
    conn = get_db_connection()
    
    # Base query
    query = '''
        SELECT s.name, s.student_id, a.marked_at, ses.subject, ses.lecture_time
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        JOIN sessions ses ON a.session_id = ses.id
        WHERE ses.subject = (SELECT name FROM subjects WHERE id = ?)
    '''
    
    params = [subject_id]
    
    if date_filter:
        query += ' AND DATE(a.marked_at) = ?'
        params.append(date_filter)
    
    query += ' ORDER BY a.marked_at DESC'
    
    attendance_records = conn.execute(query, params).fetchall()
    conn.close()
    
    attendance_data = []
    for record in attendance_records:
        attendance_data.append({
            'student_name': record['name'],
            'student_id': record['student_id'],
            'subject': record['subject'],
            'lecture_time': record['lecture_time'],
            'marked_at': record['marked_at']
        })
    
    return jsonify(attendance_data)

@app.route('/download_attendance_csv/<int:subject_id>')
@login_required
def download_attendance_csv(subject_id):
    if session.get('role') != 'teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    import csv
    from io import StringIO
    
    conn = get_db_connection()
    subject = conn.execute('SELECT name FROM subjects WHERE id = ?', (subject_id,)).fetchone()
    
    attendance_records = conn.execute('''
        SELECT s.name, s.student_id, a.marked_at, ses.lecture_time
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        JOIN sessions ses ON a.session_id = ses.id
        WHERE ses.subject = ?
        ORDER BY a.marked_at DESC
    ''', (subject['name'],)).fetchall()
    
    conn.close()
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Student Name', 'Student ID', 'Date', 'Time', 'Lecture Time'])
    
    # Write data
    for record in attendance_records:
        writer.writerow([
            record['name'],
            record['student_id'],
            record['marked_at'].split(' ')[0],
            record['marked_at'].split(' ')[1],
            record['lecture_time']
        ])
    
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
    
    # Get subject name
    subject = conn.execute('SELECT name FROM subjects WHERE id = ?', (subject_id,)).fetchone()
    
    # Get leave applications for students in this subject
    applications = conn.execute('''
        SELECT la.*, s.name as student_name
        FROM leave_applications la
        JOIN students s ON la.student_id = s.student_id
        ORDER BY la.applied_at DESC
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
            'applied_at': app['applied_at']
        })
    
    return jsonify(apps_data)