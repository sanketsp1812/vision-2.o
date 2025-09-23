// Student Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    initializeDashboard();
    
    // Add event listeners
    addEventListeners();
});

function initializeDashboard() {
    // Dashboard initialization code
    console.log('Student dashboard initialized');
}

function addEventListeners() {
    // QR Scanner button
    const scanBtn = document.getElementById('scanQRBtn');
    if (scanBtn) {
        scanBtn.addEventListener('click', openQRScanner);
    }
    
    // Quick action buttons
    const actionBtns = document.querySelectorAll('.action-btn');
    actionBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.classList[1]; // Get the second class name
            handleQuickAction(action);
        });
    });
}

function openQRScanner() {
    // Show QR scanner interface
    console.log('Opening QR scanner...');
    
    // For now, show the attendance form
    const attendanceSection = document.getElementById('attendanceSection');
    if (attendanceSection) {
        attendanceSection.style.display = 'block';
        attendanceSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function handleQuickAction(action) {
    console.log('Quick action:', action);
    
    switch(action) {
        case 'browse-subjects':
            // Navigate to subjects page
            window.location.href = '/subjects';
            break;
        case 'view-attendance':
            // Navigate to attendance page
            window.location.href = '/attendance';
            break;
        case 'view-results':
            // Navigate to results page
            window.location.href = '/results';
            break;
        case 'leave-application':
            // Navigate to leave application page
            window.location.href = '/leave';
            break;
        default:
            console.log('Unknown action:', action);
    }
}

// Message navigation functions
function previousMessage() {
    console.log('Previous message');
    // Add logic to show previous message
}

function nextMessage() {
    console.log('Next message');
    // Add logic to show next message
}

// Attendance form handling
const attendanceForm = document.getElementById('attendanceForm');
if (attendanceForm) {
    attendanceForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const studentId = document.getElementById('studentId').value;
        const qrData = document.getElementById('qrData').value;
        
        if (!studentId || !qrData) {
            showMessage('Please fill in all fields', 'error');
            return;
        }
        
        // Submit attendance
        submitAttendance(studentId, qrData);
    });
}

function submitAttendance(studentId, qrData) {
    fetch('/mark_attendance', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            student_id: studentId,
            qr_data: qrData
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('Attendance marked successfully!', 'success');
            // Reset form
            document.getElementById('attendanceForm').reset();
        } else {
            showMessage(data.message || 'Failed to mark attendance', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('An error occurred. Please try again.', 'error');
    });
}

function showMessage(message, type) {
    const messageDiv = document.getElementById('message');
    if (messageDiv) {
        messageDiv.textContent = message;
        messageDiv.className = type;
        messageDiv.style.display = 'block';
        
        // Hide message after 5 seconds
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
}