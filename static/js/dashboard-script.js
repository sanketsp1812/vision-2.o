// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeInteractions();
});

// Initialize interactions
function initializeInteractions() {
    // Action items click handling
    document.addEventListener('click', function(e){
        const card = e.target.closest('.action-item');
        if (!card) return;
        
        const actionName = (card.getAttribute('data-action') || '').toLowerCase();
        
        // Add click animation
        card.style.transform = 'translateY(-8px) scale(0.95)';
        setTimeout(() => { 
            card.style.transform = 'translateY(-12px) scale(1.05)'; 
        }, 150);
        
        // Handle different actions
        if (actionName === 'browse') {
            showNotification('Browse Subjects feature coming soon!', 'info');
        } else if (actionName === 'attendance') {
            showNotification('View Attendance feature coming soon!', 'info');
        } else if (actionName === 'results') {
            showNotification('View Results feature coming soon!', 'info');
        } else if (actionName === 'leave') {
            // Leave application is handled by onclick in HTML
            return;
        } else {
            showNotification('Feature coming soon!', 'info');
        }
    });

    // Navigation items
    const navItems = document.querySelectorAll('.nav-item[data-nav]');
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            const navText = this.textContent.trim();
            if (navText === 'Logout') {
                if (confirm('Are you sure you want to logout?')) {
                    window.location.href = '/logout';
                }
            }
        });
    });

    // QR Scanner button
    const scanBtn = document.querySelector('.scan-btn');
    if (scanBtn) {
        scanBtn.addEventListener('click', function() {
            showNotification('QR Scanner activated!', 'success');
        });
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
        <button class="notification-close">&times;</button>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-weight: 500;
        animation: slideInRight 0.3s ease;
        max-width: 400px;
    `;
    
    document.body.appendChild(notification);
    
    // Close button
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.style.cssText = `
        background: none;
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0;
        margin-left: auto;
    `;
    
    closeBtn.addEventListener('click', () => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    });
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }
    }, 4000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);