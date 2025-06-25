// ===== GDG Andalucía - Main JavaScript =====

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // ===== Initialize all functionality =====
    initializeNavigation();
    initializeButtons();
    initializeCommunityCards();
    initializeScrollEffects();
    initializeAccessibility();
    
    console.log('🚀 GDG Andalucía website loaded successfully!');
});

// ===== Navigation Functionality =====
function initializeNavigation() {
    const header = document.getElementById('header');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Smooth scrolling for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                const headerHeight = header.offsetHeight;
                const targetPosition = targetSection.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Update active navigation state
                updateActiveNavigation(targetId);
            }
        });
    });
    
    // Header scroll effect
    let lastScrollTop = 0;
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add/remove scrolled class for styling
        if (scrollTop > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        // Hide/show header on scroll (optional)
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            header.style.transform = 'translateY(-100%)';
        } else {
            header.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
}

// ===== Button Functionality =====
function initializeButtons() {
    const exploreBtn = document.getElementById('explore-btn');
    const joinBtn = document.getElementById('join-btn');
    
    // Explore Communities button
    if (exploreBtn) {
        exploreBtn.addEventListener('click', function() {
            const communitiesSection = document.getElementById('comunidades');
            const headerHeight = document.getElementById('header').offsetHeight;
            
            window.scrollTo({
                top: communitiesSection.offsetTop - headerHeight,
                behavior: 'smooth'
            });
            
            // Add visual feedback
            this.classList.add('clicked');
            setTimeout(() => this.classList.remove('clicked'), 200);
        });
    }
    
    // Join Us button
    if (joinBtn) {
        joinBtn.addEventListener('click', function() {
            // For now, show a placeholder message
            showNotification('¡Gracias por tu interés! Próximamente podrás unirte a nuestras comunidades.', 'info');
            
            // Add visual feedback
            this.classList.add('clicked');
            setTimeout(() => this.classList.remove('clicked'), 200);
        });
    }
}

// ===== Community Cards Functionality =====
function initializeCommunityCards() {
    const communityCards = document.querySelectorAll('.community-card');
    
    communityCards.forEach(card => {
        // Click handler for community cards
        card.addEventListener('click', function() {
            const communityName = this.querySelector('.community-name').textContent;
            showNotification(`¡Próximamente más información sobre ${communityName}!`, 'info');
            
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
        
        // Hover effects with enhanced interactivity
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
        
        // Keyboard navigation support
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
        
        // Make cards focusable
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', `Ver detalles de ${card.querySelector('.community-name').textContent}`);
    });
}

// ===== Scroll Effects =====
function initializeScrollEffects() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe sections for animation
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        observer.observe(section);
    });
    
    // Parallax effect for hero section (subtle)
    const hero = document.querySelector('.hero');
    if (hero) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            hero.style.transform = `translateY(${rate}px)`;
        });
    }
}

// ===== Accessibility Features =====
function initializeAccessibility() {
    // Skip to main content link
    const skipLink = document.createElement('a');
    skipLink.href = '#comunidades';
    skipLink.textContent = 'Saltar al contenido principal';
    skipLink.className = 'skip-link';
    skipLink.style.cssText = `
        position: absolute;
        top: -40px;
        left: 6px;
        background: var(--primary-green);
        color: white;
        padding: 8px;
        text-decoration: none;
        border-radius: 4px;
        z-index: 1001;
        transition: top 0.3s;
    `;
    
    skipLink.addEventListener('focus', function() {
        this.style.top = '6px';
    });
    
    skipLink.addEventListener('blur', function() {
        this.style.top = '-40px';
    });
    
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Keyboard navigation improvements
    document.addEventListener('keydown', function(e) {
        // Escape key to close any open modals/notifications
        if (e.key === 'Escape') {
            closeAllNotifications();
        }
    });
}

// ===== Utility Functions =====

// Update active navigation state
function updateActiveNavigation(activeId) {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${activeId}`) {
            link.classList.add('active');
        }
    });
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="material-icons">${type === 'info' ? 'info' : 'check_circle'}</span>
            <p>${message}</p>
            <button class="notification-close" aria-label="Cerrar notificación">
                <span class="material-icons">close</span>
            </button>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'info' ? 'var(--primary-green)' : 'var(--accent-green)'};
        color: white;
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        max-width: 400px;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    notification.querySelector('.notification-content').style.cssText = `
        display: flex;
        align-items: center;
        gap: 12px;
    `;
    
    notification.querySelector('.notification-close').style.cssText = `
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        padding: 4px;
        border-radius: 4px;
        margin-left: auto;
    `;
    
    // Add to DOM
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Close button functionality
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        closeNotification(notification);
    });
    
    // Auto-close after 5 seconds
    setTimeout(() => {
        closeNotification(notification);
    }, 5000);
}

function closeNotification(notification) {
    notification.style.transform = 'translateX(100%)';
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 300);
}

function closeAllNotifications() {
    const notifications = document.querySelectorAll('.notification');
    notifications.forEach(notification => {
        closeNotification(notification);
    });
}

// ===== Performance Optimizations =====

// Debounce function for scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for performance
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ===== Analytics and Tracking (Placeholder) =====
function trackEvent(eventName, eventData = {}) {
    // Placeholder for analytics tracking
    console.log('📊 Event tracked:', eventName, eventData);
    
    // Example implementation for Google Analytics
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, eventData);
    }
}

// Track page views and interactions
document.addEventListener('DOMContentLoaded', function() {
    trackEvent('page_view', {
        page_title: 'GDG Andalucía - Home',
        page_location: window.location.href
    });
});

// Track community card clicks
document.addEventListener('click', function(e) {
    if (e.target.closest('.community-card')) {
        const card = e.target.closest('.community-card');
        const communityName = card.querySelector('.community-name').textContent;
        trackEvent('community_card_click', {
            community_name: communityName
        });
    }
});

// ===== Error Handling =====
window.addEventListener('error', function(e) {
    console.error('❌ JavaScript error:', e.error);
    // In production, you might want to send this to an error tracking service
});

// ===== Service Worker Registration (Future Enhancement) =====
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Uncomment when you have a service worker file
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered'))
        //     .catch(error => console.log('SW registration failed'));
    });
}

// ===== Export for potential module usage =====
window.GDGAndalucia = {
    showNotification,
    trackEvent,
    closeAllNotifications
}; 