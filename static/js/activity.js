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

    // Handle quick actions
    const quickActions = document.querySelectorAll('.quick-action');
    quickActions.forEach(action => {
        action.addEventListener('click', function() {
            const actionType = this.classList[1];
            handleQuickAction(actionType);
        });
    });

    // Handle event registration buttons
    const registerBtns = document.querySelectorAll('.register-btn');
    registerBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            handleEventRegistration();
        });
    });

    // Handle view details buttons
    const detailsBtns = document.querySelectorAll('.details-btn');
    detailsBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            handleViewDetails();
        });
    });

    // Handle other buttons
    const setGoalsBtn = document.querySelector('.btn-goals');
    if (setGoalsBtn) {
        setGoalsBtn.addEventListener('click', () => alert('Set Goals feature coming soon!'));
    }

    const learnMoreBtn = document.querySelector('.btn-learn');
    if (learnMoreBtn) {
        learnMoreBtn.addEventListener('click', () => alert('Learn More feature coming soon!'));
    }

    const getStartedBtn = document.querySelector('.get-started-btn');
    if (getStartedBtn) {
        getStartedBtn.addEventListener('click', () => alert('Get Started feature coming soon!'));
    }

    const viewAllBtn = document.querySelector('.view-all-btn');
    if (viewAllBtn) {
        viewAllBtn.addEventListener('click', () => alert('View All Events feature coming soon!'));
    }

    const reminderBtn = document.querySelector('.reminder-btn');
    if (reminderBtn) {
        reminderBtn.addEventListener('click', () => alert('Set Reminders feature coming soon!'));
    }

    // Handle search
    const searchInput = document.querySelector('.search-box input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            // Implement search functionality
            console.log('Searching for:', this.value);
        });
    }

    // Handle filter
    const filterBtn = document.querySelector('.filter-btn');
    if (filterBtn) {
        filterBtn.addEventListener('click', () => alert('Filter feature coming soon!'));
    }
});

function handleQuickAction(actionType) {
    switch(actionType) {
        case 'mark-attendance':
            window.location.href = '/';
            break;
        case 'join-competition':
            alert('Join Competition feature coming soon!');
            break;
        case 'start-learning':
            alert('Start Learning feature coming soon!');
            break;
        case 'study-groups':
            alert('Study Groups feature coming soon!');
            break;
        case 'cultural-events':
            alert('Cultural Events feature coming soon!');
            break;
        case 'sports-hub':
            alert('Sports Hub feature coming soon!');
            break;
        case 'certifications':
            alert('Certifications feature coming soon!');
            break;
        case 'quick-quiz':
            alert('Quick Quiz feature coming soon!');
            break;
        default:
            console.log('Unknown action:', actionType);
    }
}

function handleEventRegistration() {
    alert('Event registration feature coming soon!');
}

function handleViewDetails() {
    alert('View event details feature coming soon!');
}

// Add smooth scrolling for better UX
function smoothScrollTo(element) {
    element.scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
    });
}