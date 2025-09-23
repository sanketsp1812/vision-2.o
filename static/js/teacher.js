document.addEventListener('DOMContentLoaded', function() {
    // Handle navigation
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            if (this.getAttribute('href') === '#') {
                e.preventDefault();
            }
        });
    });

    // QR Generation
    const generateQRBtn = document.getElementById('generateQRBtn');
    if (generateQRBtn) {
        generateQRBtn.addEventListener('click', generateQRCode);
    }
    
    const generateQR = document.getElementById('generateQR');
    if (generateQR) {
        generateQR.addEventListener('click', generateQRCode);
    }

    // Load students on page load
    loadStudents();
    loadAttendanceData();
});

function generateQR() {
    const qrSection = document.getElementById('qrSection');
    qrSection.style.display = 'block';
    qrSection.scrollIntoView({ behavior: 'smooth' });
}

function viewStudents() {
    const studentsSection = document.getElementById('studentsSection');
    studentsSection.style.display = 'block';
    studentsSection.scrollIntoView({ behavior: 'smooth' });
    loadStudents();
}

function viewReports() {
    // Implement reports functionality
    alert('Reports functionality coming soon!');
}

async function generateQRCode() {
    // Show form first
    const qrDisplay = document.getElementById('qrDisplay');
    qrDisplay.innerHTML = `
        <div class="qr-form">
            <h4>Generate QR Code</h4>
            <input type="text" id="subject" placeholder="Subject" required>
            <input type="text" id="lectureTime" placeholder="Lecture Time" required>
            <input type="text" id="location" placeholder="Location" required>
            <select id="expiryMinutes">
                <option value="5">5 minutes</option>
                <option value="10">10 minutes</option>
                <option value="15">15 minutes</option>
                <option value="20">20 minutes</option>
            </select>
            <button onclick="submitQRForm()" class="generate-btn">Generate QR</button>
            <button onclick="cancelQRForm()" class="cancel-btn">Cancel</button>
        </div>
    `;
}

window.submitQRForm = async function() {
    const subject = document.getElementById('subject').value;
    const lectureTime = document.getElementById('lectureTime').value;
    const location = document.getElementById('location').value;
    const expiryMinutes = document.getElementById('expiryMinutes').value;

    if (!subject || !lectureTime || !location) {
        alert('Please fill all fields');
        return;
    }

    try {
        const response = await fetch('/generate_qr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                subject,
                lecture_time: lectureTime,
                location,
                expiry_minutes: expiryMinutes
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            const qrDisplay = document.getElementById('qrDisplay');
            qrDisplay.innerHTML = `
                <div style="text-align: center; color: white;">
                    <img src="${data.qr_code}" alt="QR Code" style="width: 250px; height: 250px; border-radius: 10px; margin-bottom: 15px;">
                    <div style="background: rgba(255,255,255,0.9); color: #333; padding: 10px; border-radius: 10px; margin-bottom: 15px;">
                        <p style="margin: 5px 0; font-weight: 600; background: #f8f9fa; padding: 8px; border-radius: 5px; border: 1px solid #e9ecef;">${subject} - ${lectureTime}</p>
                        <p style="margin: 5px 0; background: #f8f9fa; padding: 8px; border-radius: 5px; border: 1px solid #e9ecef;">Location: ${location}</p>
                        <div class="countdown" id="countdown">Expires in: <span id="timer"></span></div>
                    </div>
                    <button onclick="window.location.reload()" style="background: #8B5CF6; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; cursor: pointer;">Back to Dashboard</button>
                </div>
            `;
            startCountdown(parseInt(expiryMinutes) * 60);
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        alert('Error generating QR code');
    }
};

window.cancelQRForm = function() {
    const qrDisplay = document.getElementById('qrDisplay');
    qrDisplay.innerHTML = '<p>Click "Generate QR" to create a new attendance session.</p>';
};

function startCountdown(seconds) {
    const timerElement = document.getElementById('timer');
    
    const countdownInterval = setInterval(() => {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        
        timerElement.textContent = `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
        
        if (seconds <= 0) {
            clearInterval(countdownInterval);
            timerElement.textContent = 'EXPIRED';
            timerElement.style.color = 'red';
        }
        
        seconds--;
    }, 1000);
}

async function loadStudents() {
    try {
        const response = await fetch('/get_students');
        const students = await response.json();
        
        const studentsGrid = document.getElementById('studentsGrid');
        if (studentsGrid && students.length > 0) {
            studentsGrid.innerHTML = students.map(student => `
                <div class="student-card">
                    <h4>${student.name}</h4>
                    <p>ID: ${student.student_id}</p>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading students:', error);
    }
}

async function loadAttendanceData() {
    try {
        const response = await fetch('/get_attendance');
        const attendanceData = await response.json();
        
        // Update activity list with real data if needed
        console.log('Attendance data loaded:', attendanceData);
    } catch (error) {
        console.error('Error loading attendance data:', error);
    }
}