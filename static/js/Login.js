document.addEventListener('DOMContentLoaded', function() {
    var registerButton = document.querySelector('form#loginForm button[type="button"]');
    registerButton.addEventListener('click', function(event) {
        event.preventDefault();
        redirectToHome();
    });

    function redirectToHome() {
        var currentUrl = window.location.href;
        var baseUrl = currentUrl.split('/').slice(0, 3).join('/'); // Extract base URL (protocol://domain:port)
        window.location.href = baseUrl + '/Register';
    }
});

        // var currentUrl = window.location.href;
        // var baseUrl = currentUrl.split('/').slice(0, 3).join('/'); // Extract base URL (protocol://domain:port)
        // window.location.href = baseUrl + '/Register';
        // replace the redirectToHome() function with these for deployment