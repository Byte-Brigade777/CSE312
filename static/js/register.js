document.addEventListener('DOMContentLoaded', function() {
    var loginLink = document.querySelector('form#registrationForm button[type="button"]');
    loginLink.addEventListener('click', function(event) {
        event.preventDefault();
        redirectToLogin(); 
    });

    function redirectToLogin() {
        window.location.href = 'http://localhost:8080'; 
    }
});