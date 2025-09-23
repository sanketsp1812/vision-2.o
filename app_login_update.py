# Updated login route for app.py
# Replace the existing login route with this code:

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form.get('user_type', 'student')  # Get user type from form
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            # Check if user type matches the selected role
            if user['role'] != user_type:
                flash(f'Invalid credentials for {user_type} login')
                return render_template('login_new.html')  # Use the new template
                
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
            flash('Invalid username or password')
    
    return render_template('login_new.html')  # Use the new template