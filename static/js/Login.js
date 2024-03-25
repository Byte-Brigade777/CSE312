document.addEventListener('DOMContentLoaded', function() {
    var registerButton = document.querySelector('form#loginForm button[type="button"]');
    registerButton.addEventListener('click', function(event) {
        event.preventDefault();
        redirectToHome();
    });

    function redirectToHome() {
        window.location.href = 'http://127.0.0.1:8080/Register';
    }
});