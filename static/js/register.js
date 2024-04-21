document.addEventListener('DOMContentLoaded', function() {
    var loginLink = document.querySelector('form#registrationForm button[type="button"]');
    loginLink.addEventListener('click', function(event) {
        event.preventDefault();
        redirectToLogin(); 
    });

    function redirectToLogin() {
        var currentUrl = window.location.href;
        var baseUrl = currentUrl.split('/').slice(0, 3).join('/'); // Extract base URL (protocol://domain:port)
        window.location.href = baseUrl; 
    }
});