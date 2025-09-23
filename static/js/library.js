document.addEventListener('DOMContentLoaded', function() {
    initializeLibrary();
    setupMouseEvents();
    setupAnimations();
    setupTooltips();
});

function initializeLibrary() {
    const browseBtn = document.querySelector('.btn-browse');
    const cardBtn = document.querySelector('.btn-card');
    
    if (browseBtn) {
        browseBtn.addEventListener('click', showSearch);
    }
    
    if (cardBtn) {
        cardBtn.addEventListener('click', showCard);
    }

    const cardActions = document.querySelectorAll('.card-action');
    cardActions.forEach(btn => {
        btn.addEventListener('click', function() {
            const actionText = this.textContent.trim();
            showNotification(`${actionText} feature activated!`, 'success');
        });
    });

    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchBooks();
            }
        });
        
        searchInput.addEventListener('input', function() {
            if (this.value.length > 2) {
                showSearchSuggestions(this.value);
            }
        });
    }

    setupFAQs();
    setupCategoryFilters();
    setupBookInteractions();
}

function setupMouseEvents() {
    // Service cards hover effects
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
            this.style.boxShadow = '0 15px 35px rgba(138, 43, 226, 0.3)';
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.1)';
        });
    });

    // Book covers hover effects
    const bookCovers = document.querySelectorAll('.book-cover, .featured-book');
    bookCovers.forEach(book => {
        book.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05) rotateY(5deg)';
            this.style.boxShadow = '0 10px 25px rgba(0,0,0,0.3)';
            this.style.transition = 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
            
            // Add glow effect
            this.style.filter = 'brightness(1.1)';
        });
        
        book.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotateY(0deg)';
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.2)';
            this.style.filter = 'brightness(1)';
        });
        
        book.addEventListener('click', function() {
            const title = this.querySelector('h4')?.textContent || 'Unknown Book';
            const author = this.querySelector('p')?.textContent || 'Unknown Author';
            openBookPreview(title, author);
        });
    });

    // Button hover effects
    const buttons = document.querySelectorAll('button, .btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 8px 20px rgba(138, 43, 226, 0.4)';
            this.style.transition = 'all 0.2s ease';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
        
        btn.addEventListener('mousedown', function() {
            this.style.transform = 'translateY(1px) scale(0.98)';
        });
        
        btn.addEventListener('mouseup', function() {
            this.style.transform = 'translateY(-2px) scale(1)';
        });
    });

    // Category tags interactive effects
    const categoryTags = document.querySelectorAll('.category-tag');
    categoryTags.forEach(tag => {
        tag.addEventListener('mouseenter', function() {
            if (!this.classList.contains('active')) {
                this.style.backgroundColor = '#e0e7ff';
                this.style.transform = 'scale(1.05)';
            }
        });
        
        tag.addEventListener('mouseleave', function() {
            if (!this.classList.contains('active')) {
                this.style.backgroundColor = '';
                this.style.transform = 'scale(1)';
            }
        });
    });
}

function showSearch() {
    const searchSection = document.getElementById('searchSection');
    if (searchSection) {
        searchSection.style.display = 'block';
        searchSection.style.opacity = '0';
        searchSection.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            searchSection.style.transition = 'all 0.5s ease';
            searchSection.style.opacity = '1';
            searchSection.style.transform = 'translateY(0)';
        }, 10);
        
        searchSection.scrollIntoView({ behavior: 'smooth' });
        
        // Focus on search input
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            setTimeout(() => searchInput.focus(), 600);
        }
    }
}

function closeSearch() {
    const searchSection = document.getElementById('searchSection');
    if (searchSection) {
        searchSection.style.opacity = '0';
        searchSection.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            searchSection.style.display = 'none';
        }, 500);
    }
}

function showCard() {
    const cardSection = document.getElementById('cardSection');
    if (cardSection) {
        cardSection.style.display = 'block';
        cardSection.style.opacity = '0';
        cardSection.style.transform = 'scale(0.9)';
        
        setTimeout(() => {
            cardSection.style.transition = 'all 0.4s ease';
            cardSection.style.opacity = '1';
            cardSection.style.transform = 'scale(1)';
        }, 10);
        
        cardSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function closeCard() {
    const cardSection = document.getElementById('cardSection');
    if (cardSection) {
        cardSection.style.opacity = '0';
        cardSection.style.transform = 'scale(0.9)';
        setTimeout(() => {
            cardSection.style.display = 'none';
        }, 400);
    }
}

function searchBooks() {
    const query = document.getElementById('searchInput').value;
    if (!query.trim()) {
        showNotification('Please enter a search term', 'warning');
        return;
    }
    
    showLoadingSpinner();
    
    // Simulate API call delay
    setTimeout(() => {
        const results = [
            { title: 'JavaScript: The Definitive Guide', author: 'David Flanagan', category: 'Programming', available: true, rating: 4.5 },
            { title: 'Python Crash Course', author: 'Eric Matthes', category: 'Programming', available: true, rating: 4.8 },
            { title: 'Clean Code', author: 'Robert Martin', category: 'Programming', available: false, rating: 4.7 },
            { title: 'Calculus: Early Transcendentals', author: 'James Stewart', category: 'Mathematics', available: true, rating: 4.3 },
            { title: 'Introduction to Algorithms', author: 'Thomas Cormen', category: 'Computer Science', available: true, rating: 4.6 },
            { title: 'The Great Gatsby', author: 'F. Scott Fitzgerald', category: 'Literature', available: true, rating: 4.2 }
        ];
        
        const filteredResults = results.filter(book => 
            book.title.toLowerCase().includes(query.toLowerCase()) ||
            book.author.toLowerCase().includes(query.toLowerCase()) ||
            book.category.toLowerCase().includes(query.toLowerCase())
        );
        
        hideLoadingSpinner();
        displaySearchResults(filteredResults, query);
        
        if (filteredResults.length > 0) {
            showNotification(`Found ${filteredResults.length} book(s) matching "${query}"`, 'success');
        }
    }, 800);
}

function displaySearchResults(results, query) {
    const resultsContainer = document.getElementById('searchResults');
    
    if (results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="no-results">
                <i class="fas fa-search" style="font-size: 3rem; color: #ccc; margin-bottom: 1rem;"></i>
                <h3>No books found for "${query}"</h3>
                <p>Try different keywords or browse our categories</p>
                <button onclick="showAllBooks()" class="btn-primary">Browse All Books</button>
            </div>
        `;
        return;
    }
    
    resultsContainer.innerHTML = results.map((book, index) => `
        <div class="search-result-item" style="animation-delay: ${index * 0.1}s" onclick="openBookPreview('${book.title}', '${book.author}')">
            <div class="result-cover ${book.category.toLowerCase()}">
                <i class="fas fa-book"></i>
                <div class="book-rating">
                    <i class="fas fa-star"></i>
                    <span>${book.rating}</span>
                </div>
            </div>
            <div class="book-info">
                <h4>${highlightSearchTerm(book.title, query)}</h4>
                <p class="author">${highlightSearchTerm(book.author, query)}</p>
                <span class="category-badge">${book.category}</span>
                <div class="availability ${book.available ? 'available' : 'unavailable'}">
                    <i class="fas ${book.available ? 'fa-check-circle' : 'fa-times-circle'}"></i>
                    ${book.available ? 'Available' : 'Checked Out'}
                </div>
            </div>
            <div class="book-actions">
                ${book.available ? 
                    `<button class="btn-borrow" onclick="event.stopPropagation(); borrowBook('${book.title}')">Borrow</button>` :
                    `<button class="btn-reserve" onclick="event.stopPropagation(); reserveBook('${book.title}')">Reserve</button>`
                }
                <button class="btn-preview" onclick="event.stopPropagation(); openBookPreview('${book.title}', '${book.author}')">Preview</button>
            </div>
        </div>
    `).join('');
    
    // Animate results
    const items = resultsContainer.querySelectorAll('.search-result-item');
    items.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        setTimeout(() => {
            item.style.transition = 'all 0.5s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

function openBookPreview(title, author) {
    // Create modal overlay
    const modal = document.createElement('div');
    modal.className = 'book-preview-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>${title}</h2>
                <span class="close-modal" onclick="closeBookPreview()">&times;</span>
            </div>
            <div class="modal-body">
                <div class="book-preview-cover">
                    <i class="fas fa-book-open"></i>
                </div>
                <div class="book-details">
                    <p><strong>Author:</strong> ${author}</p>
                    <p><strong>Pages:</strong> 324</p>
                    <p><strong>Published:</strong> 2023</p>
                    <p><strong>Genre:</strong> Educational</p>
                    <div class="book-rating">
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="far fa-star"></i>
                        <span>4.2/5</span>
                    </div>
                    <p class="book-description">
                        This comprehensive guide provides in-depth coverage of the subject matter with practical examples and exercises.
                    </p>
                </div>
            </div>
            <div class="modal-actions">
                <button onclick="borrowBook('${title}')" class="btn-primary">Borrow Book</button>
                <button onclick="addToWishlist('${title}')" class="btn-secondary">Add to Wishlist</button>
                <button onclick="readSample('${title}')" class="btn-outline">Read Sample</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Animate modal appearance
    setTimeout(() => {
        modal.style.opacity = '1';
        modal.querySelector('.modal-content').style.transform = 'scale(1)';
    }, 10);
}

function closeReader() {
    const readerSection = document.getElementById('readerSection');
    if (readerSection) {
        readerSection.style.opacity = '0';
        readerSection.style.transform = 'scale(0.95)';
        setTimeout(() => {
            readerSection.style.display = 'none';
        }, 300);
    }
}

function nextPage() {
    const current = parseInt(document.getElementById('currentPage')?.textContent || '1');
    const total = parseInt(document.getElementById('totalPages')?.textContent || '100');
    if (current < total) {
        document.getElementById('currentPage').textContent = current + 1;
        showNotification(`Page ${current + 1}`, 'info');
    } else {
        showNotification('You\'re on the last page', 'warning');
    }
}

function previousPage() {
    const current = parseInt(document.getElementById('currentPage')?.textContent || '1');
    if (current > 1) {
        document.getElementById('currentPage').textContent = current - 1;
        showNotification(`Page ${current - 1}`, 'info');
    } else {
        showNotification('You\'re on the first page', 'warning');
    }
}

function toggleBookmark() {
    const btn = document.getElementById('bookmarkBtn');
    if (!btn) return;
    
    const icon = btn.querySelector('i');
    
    if (icon.classList.contains('far')) {
        icon.classList.remove('far');
        icon.classList.add('fas');
        btn.style.color = '#ff6b6b';
        showNotification('Book bookmarked!', 'success');
    } else {
        icon.classList.remove('fas');
        icon.classList.add('far');
        btn.style.color = '';
        showNotification('Bookmark removed!', 'info');
    }
    
    // Add bounce animation
    btn.style.transform = 'scale(1.2)';
    setTimeout(() => {
        btn.style.transform = 'scale(1)';
    }, 200);
}

function showAllBooks() {
    showSearch();
    // Pre-populate with all books
    setTimeout(() => {
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.value = '';
            searchBooks();
        }
    }, 600);
}

function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.opacity = '0';
        tab.style.transform = 'translateX(-20px)';
        setTimeout(() => {
            tab.style.display = 'none';
        }, 200);
    });
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    setTimeout(() => {
        const targetTab = document.getElementById(tabName + 'Tab');
        if (targetTab) {
            targetTab.style.display = 'block';
            setTimeout(() => {
                targetTab.style.opacity = '1';
                targetTab.style.transform = 'translateX(0)';
            }, 10);
        }
        event.target.classList.add('active');
    }, 200);
}

function borrowBook(title) {
    showConfirmDialog(
        'Confirm Borrow',
        `Do you want to borrow "${title}"?`,
        () => {
            showNotification(`"${title}" has been reserved for you! Visit library within 24 hours to collect.`, 'success');
            closeBookPreview();
            updateBorrowedBooks(title);
        }
    );
}

function reserveBook(title) {
    showNotification(`"${title}" has been added to your reservation list. You'll be notified when it's available.`, 'info');
}

function addToWishlist(title) {
    showNotification(`"${title}" added to your wishlist!`, 'success');
    closeBookPreview();
}

function readSample(title) {
    showNotification('Opening sample pages...', 'info');
    closeBookPreview();
    // Simulate opening reader
    setTimeout(() => {
        openReader(title);
    }, 500);
}

function renewBook(bookId) {
    showConfirmDialog(
        'Renew Book',
        'Extend borrowing period by 14 days?',
        () => {
            showNotification('Book renewed! New due date: Jan 15, 2025', 'success');
        }
    );
}

function returnBook(bookId) {
    showConfirmDialog(
        'Return Book',
        'Are you sure you want to return this book?',
        () => {
            showNotification('Book return initiated. Thank you!', 'success');
        }
    );
}

function downloadCard() {
    showNotification('Generating library card...', 'info');
    setTimeout(() => {
        showNotification('Library card downloaded successfully!', 'success');
    }, 1500);
}

function showQRCode() {
    const modal = document.createElement('div');
    modal.className = 'qr-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>Your Library QR Code</h3>
                <span class="close-modal" onclick="this.closest('.qr-modal').remove()">&times;</span>
            </div>
            <div class="qr-code-container">
                <div class="qr-code">
                    <div class="qr-pattern"></div>
                </div>
                <p>Show this QR code at the library for quick access</p>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

// Enhanced category switching with animations
function switchCategory(category) {
    document.querySelectorAll('.category-tag').forEach(tag => {
        tag.classList.remove('active');
    });
    
    event.target.classList.add('active');
    
    // Animate category books
    const categoryBooks = document.querySelectorAll('.category-books .book-cover');
    categoryBooks.forEach((book, index) => {
        book.style.opacity = '0';
        book.style.transform = 'scale(0.8)';
        
        setTimeout(() => {
            book.style.transition = 'all 0.3s ease';
            book.style.opacity = '1';
            book.style.transform = 'scale(1)';
        }, index * 50);
    });
    
    showNotification(`Showing ${category} books`, 'info');
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas ${getNotificationIcon(type)}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">&times;</button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 10);
    
    setTimeout(() => {
        notification.remove();
    }, 4000);
}

function getNotificationIcon(type) {
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    return icons[type] || icons.info;
}

function showLoadingSpinner() {
    const spinner = document.createElement('div');
    spinner.id = 'loadingSpinner';
    spinner.className = 'loading-spinner';
    spinner.innerHTML = '<div class="spinner"></div><p>Searching books...</p>';
    document.body.appendChild(spinner);
}

function hideLoadingSpinner() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) spinner.remove();
}

function highlightSearchTerm(text, term) {
    if (!term) return text;
    const regex = new RegExp(`(${term})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

function showConfirmDialog(title, message, onConfirm) {
    const dialog = document.createElement('div');
    dialog.className = 'confirm-dialog';
    dialog.innerHTML = `
        <div class="dialog-content">
            <h3>${title}</h3>
            <p>${message}</p>
            <div class="dialog-actions">
                <button onclick="this.closest('.confirm-dialog').remove()" class="btn-secondary">Cancel</button>
                <button onclick="confirmAction()" class="btn-primary">Confirm</button>
            </div>
        </div>
    `;
    
    dialog.querySelector('.btn-primary').onclick = () => {
        onConfirm();
        dialog.remove();
    };
    
    document.body.appendChild(dialog);
}

function closeBookPreview() {
    const modal = document.querySelector('.book-preview-modal');
    if (modal) {
        modal.style.opacity = '0';
        modal.querySelector('.modal-content').style.transform = 'scale(0.8)';
        setTimeout(() => modal.remove(), 300);
    }
}

function setupAnimations() {
    // Add scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.service-card, .featured-book, .library-notice').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
}

function setupTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(el => {
        el.addEventListener('mouseenter', showTooltip);
        el.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = e.target.dataset.tooltip;
    document.body.appendChild(tooltip);
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
}

function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) tooltip.remove();
}

function setupFAQs() {
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        if (question) {
            question.addEventListener('click', () => {
                const answer = item.querySelector('.faq-answer');
                const isOpen = item.classList.contains('open');
                
                // Close all other FAQs
                faqItems.forEach(otherItem => {
                    otherItem.classList.remove('open');
                });
                
                if (!isOpen) {
                    item.classList.add('open');
                }
            });
        }
    });
}

function setupCategoryFilters() {
    const categoryTags = document.querySelectorAll('.category-tag');
    categoryTags.forEach(tag => {
        tag.addEventListener('click', function() {
            switchCategory(this.textContent);
        });
    });
}

function setupBookInteractions() {
    // Add double-click to open book preview
    const books = document.querySelectorAll('.book-cover, .featured-book');
    books.forEach(book => {
        book.addEventListener('dblclick', function() {
            const title = this.querySelector('h4')?.textContent || 'Sample Book';
            const author = this.querySelector('p')?.textContent || 'Unknown Author';
            openBookPreview(title, author);
        });
    });
}

function showSearchSuggestions(query) {
    const suggestions = ['JavaScript', 'Python', 'Mathematics', 'Literature', 'Science', 'History'];
    const filtered = suggestions.filter(s => s.toLowerCase().includes(query.toLowerCase()));
    
    if (filtered.length > 0) {
        // Implementation for search suggestions dropdown
        console.log('Suggestions:', filtered);
    }
}

function updateBorrowedBooks(title) {
    // Update user's borrowed books list
    const borrowedBooks = JSON.parse(localStorage.getItem('borrowedBooks') || '[]');
    borrowedBooks.push({
        title: title,
        borrowDate: new Date().toISOString(),
        dueDate: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString()
    });
    localStorage.setItem('borrowedBooks', JSON.stringify(borrowedBooks));
}

function openReader(title) {
    showNotification(`Opening "${title}" in reader mode...`, 'info');
    // Implementation for book reader
}