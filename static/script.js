// Add to cart functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize any interactive elements
    console.log('ShopHub E-Commerce site loaded!');
    
    // Add to cart buttons
    const cartButtons = document.querySelectorAll('.btn-primary');
    cartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!this.disabled) {
                const productName = this.closest('.product-detail-info')?.querySelector('h1')?.textContent || 
                                   this.closest('.product-card')?.querySelector('.product-title')?.textContent;
                
                if (productName) {
                    showNotification(`Added "${productName}" to cart!`, 'success');
                } else {
                    showNotification('Added to cart!', 'success');
                }
            }
        });
    });
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 500);
        }, 5000);
    });
});

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '1000';
    notification.style.maxWidth = '300px';
    notification.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transition = 'opacity 0.5s';
        setTimeout(() => {
            notification.remove();
        }, 500);
    }, 3000);
}

// Search functionality with debounce
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

// Optional: Add price formatting
function formatPrice(price) {
    return '$' + parseFloat(price).toFixed(2);
}

// Optional: Add rating stars display
function getStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    let stars = '⭐'.repeat(fullStars);
    if (hasHalfStar) {
        stars += '½';
    }
    return stars || 'No ratings';
}

// Expose functions globally for use in templates
window.showNotification = showNotification;
window.formatPrice = formatPrice;
window.getStars = getStars;
