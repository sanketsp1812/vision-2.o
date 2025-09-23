// Subject-specific modal functions
let currentSubjectId = null;

function openAttendanceModal(subjectName, subjectId) {
    currentSubjectId = subjectId;
    document.getElementById('attendanceModal').classList.add('active');
    document.body.style.overflow = 'hidden';
    loadSubjectAttendance(subjectId);
}

function closeAttendanceModal() {
    document.getElementById('attendanceModal').classList.remove('active');
    document.body.style.overflow = 'auto';
    currentSubjectId = null;
}

function openSubjectLeaveModal(subjectName, subjectId) {
    currentSubjectId = subjectId;
    document.getElementById('subjectLeaveModal').classList.add('active');
    document.body.style.overflow = 'hidden';
    loadSubjectLeaveApplications(subjectId);
}

function closeSubjectLeaveModal() {
    document.getElementById('subjectLeaveModal').classList.remove('active');
    document.body.style.overflow = 'auto';
    currentSubjectId = null;
}

function loadSubjectAttendance(subjectId, dateFilter = null) {
    let url = `/get_subject_attendance/${subjectId}`;
    if (dateFilter) {
        url += `?date=${dateFilter}`;
    }
    
    fetch(url)
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('attendanceList');
        if (data.length === 0) {
            container.innerHTML = '<div class="no-applications">No attendance records found.</div>';
            return;
        }
        
        let html = `
            <table class="attendance-table">
                <thead>
                    <tr>
                        <th>Student Name</th>
                        <th>Student ID</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Lecture</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        data.forEach(record => {
            const date = new Date(record.marked_at);
            html += `
                <tr>
                    <td>${record.student_name}</td>
                    <td>${record.student_id}</td>
                    <td>${date.toLocaleDateString()}</td>
                    <td>${date.toLocaleTimeString()}</td>
                    <td>${record.lecture_time}</td>
                    <td><span class="status-present">Present</span></td>
                </tr>
            `;
        });
        
        html += '</tbody></table>';
        container.innerHTML = html;
    })
    .catch(error => {
        document.getElementById('attendanceList').innerHTML = '<div class="error">Failed to load attendance.</div>';
    });
}

function loadSubjectLeaveApplications(subjectId) {
    fetch(`/get_subject_leave_applications/${subjectId}`)
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('subjectLeaveList');
        if (data.length === 0) {
            container.innerHTML = '<div class="no-applications">No leave applications found for this subject.</div>';
            return;
        }
        
        let html = '';
        data.forEach(app => {
            const statusClass = app.status === 'approved' ? 'approved' : app.status === 'rejected' ? 'rejected' : 'pending';
            html += `
                <div class="application-card">
                    <div class="app-header">
                        <div class="student-info">
                            <h4>${app.student_name}</h4>
                            <span class="student-id">ID: ${app.student_id}</span>
                        </div>
                        <div class="status-badge ${statusClass}">${app.status.toUpperCase()}</div>
                    </div>
                    <div class="app-details">
                        <div class="detail-row">
                            <span class="label">Leave Type:</span>
                            <span class="value">${app.leave_type}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Duration:</span>
                            <span class="value">${app.start_date} to ${app.end_date}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Reason:</span>
                            <span class="value">${app.reason}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Applied:</span>
                            <span class="value">${new Date(app.applied_at).toLocaleDateString()}</span>
                        </div>
                    </div>
                    ${app.status === 'pending' ? `
                        <div class="app-actions">
                            <button class="approve-btn" onclick="updateLeaveStatus(${app.id}, 'approved')">
                                <i class="fas fa-check"></i> Approve
                            </button>
                            <button class="reject-btn" onclick="updateLeaveStatus(${app.id}, 'rejected')">
                                <i class="fas fa-times"></i> Reject
                            </button>
                        </div>
                    ` : ''}
                </div>
            `;
        });
        container.innerHTML = html;
    })
    .catch(error => {
        document.getElementById('subjectLeaveList').innerHTML = '<div class="error">Failed to load applications.</div>';
    });
}

function filterAttendance() {
    const dateFilter = document.getElementById('attendanceDate').value;
    if (currentSubjectId) {
        loadSubjectAttendance(currentSubjectId, dateFilter);
    }
}

function downloadAttendanceCSV() {
    if (currentSubjectId) {
        window.open(`/download_attendance_csv/${currentSubjectId}`, '_blank');
    }
}

// Close modals when clicking outside
document.getElementById('attendanceModal').addEventListener('click', function(e) {
    if (e.target === this) closeAttendanceModal();
});

document.getElementById('subjectLeaveModal').addEventListener('click', function(e) {
    if (e.target === this) closeSubjectLeaveModal();
});