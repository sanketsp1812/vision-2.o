document.addEventListener('DOMContentLoaded', function() {
    const generateQRBtn = document.getElementById('generateQR');
    const qrDisplay = document.getElementById('qrDisplay');
    const refreshBtn = document.getElementById('refreshAttendance');
    const attendanceList = document.getElementById('attendanceList');
    let countdownInterval;

    generateQRBtn.addEventListener('click', function() {
        showQRForm();
    });

    function showQRForm() {
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
                <button onclick="generateQR()" class="generate-btn">Generate QR</button>
                <button onclick="cancelQR()" class="cancel-btn">Cancel</button>
            </div>
        `;
    }

    window.generateQR = async function() {
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
                displayQRCode(data);
                startCountdown(parseInt(expiryMinutes) * 60);
            } else {
                alert('Error: ' + data.message);
            }
        } catch (error) {
            alert('Error generating QR code');
        }
    };

    function displayQRCode(data) {
        const subject = document.getElementById('subject').value;
        const lectureTime = document.getElementById('lectureTime').value;
        const location = document.getElementById('location').value;
        
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
    }

    function startCountdown(seconds) {
        const timerElement = document.getElementById('timer');
        
        countdownInterval = setInterval(() => {
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

    window.cancelQR = function() {
        resetQR();
    };

    window.resetQR = function() {
        if (countdownInterval) {
            clearInterval(countdownInterval);
        }
        qrDisplay.innerHTML = `
            <div class="corner top-left"></div>
            <div class="corner top-right"></div>
            <div class="corner bottom-left"></div>
            <div class="corner bottom-right"></div>
            <i class="fas fa-qrcode" style="font-size: 48px; color: rgba(255,255,255,0.3);"></i>
        `;
    };

    refreshBtn.addEventListener('click', loadAttendance);

    async function loadAttendance() {
        try {
            const response = await fetch('/get_attendance');
            const attendance = await response.json();
            
            if (attendance.length === 0) {
                attendanceList.innerHTML = '<p>No attendance records found.</p>';
                return;
            }
            
            const table = `
                <table class="attendance-table">
                    <thead>
                        <tr>
                            <th>Student ID</th>
                            <th>Student Name</th>
                            <th>Session ID</th>
                            <th>Timestamp</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${attendance.map(record => `
                            <tr>
                                <td>${record.student_id}</td>
                                <td>${record.student_name}</td>
                                <td>${record.session_id}</td>
                                <td>${record.timestamp}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            
            attendanceList.innerHTML = table;
        } catch (error) {
            attendanceList.innerHTML = '<p class="error">Error loading attendance records</p>';
        }
    }

    // Load attendance on page load
    loadAttendance();
});