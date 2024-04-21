document.addEventListener('DOMContentLoaded', function() {
    var registerButton = document.querySelector('form#loginForm button[type="button"]');
    registerButton.addEventListener('click', function(event) {
        event.preventDefault();
        login();
    });

    function login() {
        var username = document.querySelector('#username').value;
        var password = document.querySelector('#password').value;

        // ajax request to login endpoint
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    window.location.href = '/Home';
                } else {
                    console.error('Login failed');
                }
            }
        }
        xhr.open('POST', '/login');
        xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
        xhr.send('username=' + encodeURIComponent(username) + '&password=' + encodeURIComponent(password));
    }
});

document.addEventListener('DOMContentLoaded',function() {
    var registerButton = document.querySelector('form#loginForm button[type="button"]');
    registerButton.addEventListener('click', function(event) {
        event.preventDefault();
        redirectToHome();
    });

    function redirectToHome() {
        window.location.href = 'http://localhost:8080/Register';
    }
})

        // var currentUrl = window.location.href;
        // var baseUrl = currentUrl.split('/').slice(0, 3).join('/'); // Extract base URL (protocol://domain:port)
        // window.location.href = currentDomain + '/Register';