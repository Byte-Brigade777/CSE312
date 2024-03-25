document.addEventListener('DOMContentLoaded', function() {
    var loginLink = document.querySelector('form#registrationForm button[type="button"]');
    loginLink.addEventListener('click', function(event) {
        event.preventDefault();
        redirectToLogin(); 
    });

    function redirectToLogin() {
        window.location.href = 'http://127.0.0.1:8080'; 
    }
});