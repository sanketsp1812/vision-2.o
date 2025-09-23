# QR Attendance System

A comprehensive web-based attendance management system with QR code functionality, built using Flask, SQLite, and modern web technologies.

## 🚀 Features

### 👨‍🎓 Student Features
- **QR Code Attendance**: Mark attendance by scanning QR codes
- **Activity Participation**: Join certificate-enabled activities
- **Certificate Download**: Download professional certificates after activity participation
- **Leave Applications**: Submit leave requests with file attachments
- **Dashboard**: View attendance statistics and activity status

### 👨‍🏫 Teacher Features
- **Subject Management**: Create and manage subjects with divisions and academic years
- **QR Code Generation**: Generate time-limited QR codes for attendance sessions
- **Activity Creation**: Create activities with certificate verification options
- **Attendance Tracking**: View and download attendance records as CSV
- **Leave Management**: Review and approve/reject student leave applications
- **Results Entry**: Manual result entry and CSV bulk upload
- **Analytics**: View attendance statistics and reports

### 🔐 Authentication System
- Role-based access control (Student/Teacher/Admin)
- Secure password hashing
- Session management
- User registration with role-specific fields

## 📋 Requirements

- Python 3.7+
- Flask 2.0+
- SQLite3
- Required Python packages (see requirements.txt)

## 🛠️ Installation

### Quick Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd qr-attendance-system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run setup script:**
   ```bash
   python setup.py
   ```

4. **Start the application:**
   ```bash
   python run.py
   ```

5. **Access the application:**
   - Open your browser and go to `http://localhost:5000`

### Manual Setup

If you prefer manual setup:

1. **Initialize database:**
   ```bash
   python database.py
   ```

2. **Run application:**
   ```bash
   python app.py
   ```

## 📊 Database Schema

### Users Table
- id, username, email, password_hash, role, created_at

### Students Table
- id, student_id, name, user_id

### Teachers Table
- id, teacher_id, name, subject, user_id

### Subjects Table
- id, name, code, academic_year, division, credits, description, semester, department, teacher_id, created_at

### Activities Table
- id, title, description, activity_type, event_date, start_time, end_time, location, max_participants, requirements, organizer, teacher_id, certificate_enabled, created_at

### Sessions Table
- id, qr_data, subject, lecture_time, location, expiry_time, created_at, is_active

### Attendance Table
- id, student_id, session_id, marked_at

### Leave Applications Table
- id, student_id, student_name, leave_type, start_date, end_date, reason, attachment_path, status, applied_at, reviewed_at, reviewed_by

### Results Table
- id, student_id, subject_id, exam_type, marks_obtained, max_marks, remarks, teacher_id, created_at

### Activity Participants Table
- id, activity_id, student_id, student_name, participated_at

## 🔑 Default Login Credentials

### Admin
- Username: `admin`
- Password: `admin123`

### Teacher
- Username: `teacher`
- Password: `teacher123`

### Student Registration
Students and teachers can register through the registration page with role-specific information.

## 📁 Project Structure

```
qr-attendance-system/
├── app.py                    # Main Flask application
├── database.py              # Database initialization and schema
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Git ignore rules
├── attendance.db           # SQLite database (auto-generated)
│
├── templates/              # Jinja2 HTML templates
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── student_dashboard.html
│   ├── teacher_dashboard.html
│   ├── admin.html          # Admin dashboard
│   ├── activity.html       # Student activity page
│   ├── teacher_activity.html
│   ├── certificate.html    # Certificate template
│   ├── qr_scanner.html     # QR code scanner
│   ├── qr_display.html     # QR code display
│   ├── subjects.html       # Subject management
│   ├── library.html        # Student library
│   ├── teacher_library.html
│   ├── analytics.html      # Analytics dashboard
│   └── attendance_modal.html
│
├── static/                 # Static assets
│   ├── css/
│   │   ├── style.css       # Main stylesheet
│   │   └── dashboard-styles.css
│   └── js/
│       ├── student.js      # Student-specific JavaScript
│       ├── teacher.js      # Teacher-specific JavaScript
│       ├── admin.js        # Admin-specific JavaScript
│       ├── activity.js     # Activity management
│       ├── library.js      # Library functionality
│       ├── dashboard-script.js
│       └── subject_modals.js
│
└── uploads/                # File upload directory
    ├── .gitkeep           # Keep directory in git
    └── leave_documents/   # Leave application attachments
```

## 🎯 Usage Guide

### For Students

1. **Login**: Use your student credentials to access the system
2. **Mark Attendance**: 
   - Go to QR Scanner
   - Scan the QR code displayed by teacher
   - Attendance will be marked automatically
3. **Join Activities**:
   - Visit Activity Hub
   - Click "Join Activity" for certificate-enabled activities
   - Download certificate after participation
4. **Submit Leave Applications**:
   - Fill leave application form
   - Attach supporting documents if required
   - Track application status

### For Teachers

1. **Create Subjects**:
   - Go to Teacher Dashboard
   - Click "Create New Subject"
   - Fill subject details including academic year and division

2. **Generate QR Codes**:
   - Select a subject
   - Click "Generate QR Code"
   - Set class timings and expiry duration
   - Display QR code for students to scan

3. **Create Activities**:
   - Go to Activity section
   - Click "Create New Activity"
   - Enable certificate option if needed
   - Students can join and download certificates

4. **Manage Results**:
   - Use Results modal for manual entry
   - Upload CSV files for bulk result entry
   - Format: student_id, name, subject_id, exam_type, marks_obtained, max_marks, remarks

5. **Review Leave Applications**:
   - View all submitted applications
   - Approve or reject with comments
   - Download attachments if provided

## 📝 CSV Upload Formats

### Results Upload
```csv
student_id,name,subject_id,exam_type,marks_obtained,max_marks,remarks
001,John Doe,1,Unit Test,85,100,Good performance
002,Jane Smith,1,Unit Test,92,100,Excellent work
```

### Student Data Import (Excel Format)
```
Sheet 1: Students
| full_name | registration_no | academic_session | email | department | current_year | password |

Sheet 2: Teachers
| full_name | teacher_id | email | department | subject | password |
```

## 🎨 Features Highlights

### QR Code System
- Time-limited QR codes (30 seconds to 20 minutes)
- Automatic expiry and session management
- Real-time attendance tracking

### Certificate System
- Professional certificate design with institution branding
- Golden color scheme with animated elements
- Downloadable/printable certificates
- Only available for participated activities

### Modern UI/UX
- Responsive design for mobile and desktop
- Interactive animations and transitions
- Glass morphism effects
- Professional dashboard layouts

### Security Features
- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control
- File upload validation

## 🔧 Configuration

### Application Settings
- **Secret Key**: Change `app.secret_key` in production
- **File Upload**: Maximum 5MB file size limit
- **Database**: SQLite with automatic initialization

### Environment Setup
```bash
# Development
export FLASK_ENV=development
export FLASK_DEBUG=1

# Production
export FLASK_ENV=production
export SECRET_KEY="your-production-secret-key"
```

### Database Configuration
- **File**: `attendance.db` (SQLite)
- **Auto-creation**: Tables created on first run
- **Backup**: Regular database backups recommended

## 🚨 Troubleshooting

### Common Issues

1. **Database not found**: Run `python database.py` to initialize
2. **Permission errors**: Ensure write permissions for database file
3. **File upload fails**: Check upload directory permissions
4. **QR codes not working**: Verify system time and expiry settings

### Debug Mode
Run with debug enabled for development:
```bash
export FLASK_DEBUG=1
python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v1.0.0**: Initial release with basic QR attendance
- **v1.1.0**: Added activity management and certificates
- **v1.2.0**: Enhanced UI/UX and result management
- **v1.3.0**: Added leave applications and analytics

---

**Built with ❤️ using Flask and modern web technologies**