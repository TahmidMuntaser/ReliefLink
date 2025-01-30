document.addEventListener('DOMContentLoaded', function() {
    const notifications = document.querySelectorAll('.notification');
    console.log('Notifications found:', notifications.length);
    
    notifications.forEach(notification => {
        console.log('Setting timeout for notification:', notification.innerText);
        setTimeout(() => {
            console.log('Adding fade-out class to notification:', notification.innerText);
            notification.classList.add('fade-out');
            
            notification.addEventListener('transitionend', () => {
                console.log('Hiding notification:', notification.innerText);
                notification.style.display = 'none';
            });
        }, 5000); 
    });
});