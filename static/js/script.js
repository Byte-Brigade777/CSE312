
document.addEventListener("DOMContentLoaded", function() {
    const ws = false;
    let socket = null;
    function initWS() {
        // Establish a WebSocket connection with the server
        socket = new WebSocket('ws://' + window.location.host + '/websocket');
    
        // Called whenever data is received from the server over the WebSocket connection
        socket.onmessage = function (ws_message) {
            const message = JSON.parse(ws_message.data);
            const messageType = message.messageType
            if(messageType === 'postMessage'){
                displayPost(message);
            }else{
                // Handle other message types if needed
            }
        }
    }

    function logout() {
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                console.log("Logout successful");
                window.location.href = "http://localhost:8080"; 
            }
        }
        request.open("GET", "/logout");
        request.send();
    }
    
    const logoutButton = document.querySelector(".logout-button");
    logoutButton.addEventListener("click", function() {
        logout();
    });
    
    function displayPost(postJSON) {
        const postsContainer = document.getElementById("posts-container");
        const postElement = document.createElement("div");
        postElement.classList.add("post");
    
        const headerElement = document.createElement("div");
        headerElement.classList.add("header");
    
        const usernameTitleElement = document.createElement("p");
        usernameTitleElement.classList.add("username-title");
        usernameTitleElement.textContent = postJSON.username + ": " + postJSON.title;
    
        const contentElement = document.createElement("p");
        contentElement.classList.add("content");
        contentElement.textContent = postJSON.content;
    
        headerElement.appendChild(usernameTitleElement);
        postElement.appendChild(headerElement);
        postElement.appendChild(contentElement);
    
        postsContainer.appendChild(postElement);
    }
    
    function sendPost() {
        const titleInput = document.querySelector(".post-title-input");
        const contentInput = document.querySelector(".post-content-input");
        
        // Retrieve values
        const title = titleInput.value;
        const content = contentInput.value;
        
        if (!title.trim() || !content.trim()) {
            console.error("Both title and content must be provided.");
            return;
        }
        
        if (ws) {
            // Using WebSockets
            socket.send(JSON.stringify({'messageType': 'postMessage', 'title': title, 'content': content}));
        } else {
            // Using AJAX
            const request = new XMLHttpRequest();
            request.onreadystatechange = function () {
                if (this.readyState === 4 && this.status === 200) {
                    console.log(this.response);
                    // If successful, refresh posts
                    updatePosts();
                    // Clear input fields
                    clearInputFields(titleInput, contentInput);
                }
            }
            const postJSON = {"title": title, "content": content};
            request.open("POST", "/add");
            request.setRequestHeader("Content-Type", "application/json");
            request.send(JSON.stringify(postJSON));
        }
    }
    
    function clearInputFields(...inputs) {
        inputs.forEach(input => {
            input.value = '';
        });
    }
    
    function updatePosts() {
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                const posts = JSON.parse(this.response);
                clearPosts();
                for (const post of posts) {
                    displayPost(post);
                }
            }
        }
        request.open("GET", "/posts");
        request.send();
    }
    
    function clearPosts() {
        const postsContainer = document.getElementById("posts-container");
        postsContainer.innerHTML = "";
    }
    
    
    setInterval(updatePosts, 5000);


    const addButton = document.querySelector(".add-post-button");
    addButton.addEventListener("click", function() {
        sendPost();
    });
});

