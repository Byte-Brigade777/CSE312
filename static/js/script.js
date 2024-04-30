
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
        console.log("Displaying post:", postJSON);  // Debug: Log post data to console

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

        if (postJSON.url) {
            const imageElement = document.createElement("img");
            imageElement.src = '/static/img/' + postJSON.url;
            imageElement.alt = "Post Image";
            imageElement.style.width = '100%';
            imageElement.onerror = function () {
                console.error("Error loading image at", this.src); 
                this.style.display = 'none'; 
            };
            postElement.appendChild(imageElement);
        }

        postsContainer.appendChild(postElement);
    }


    
    function sendPost() {
        const titleInput = document.querySelector(".post-title-input");
        const contentInput = document.querySelector(".post-content-input");
        
    
        const title = titleInput.value;
        const content = contentInput.value;
        
        if (!title.trim() || !content.trim()) {
            console.error("Both title and content must be provided.");
            return;
        }


        const fileInput = document.getElementById("file-upload");
        const hasFile = fileInput.files.length > 0;
        let uploadCompleted=false;
        const postJSON = { title, content };

        if (hasFile) {
            uploadFile();
            if (uploadResponse.success) {
                console.log("File uploaded successfully");
                postJSON.filename = uploadResponse.filename; 
            }
        }
        
        
        // if (ws) {
        //     // Using WebSockets
        //     socket.send(JSON.stringify({'messageType': 'postMessage', 'title': title, 'content': content}));
        // } 
     
                // Send the post data (including filename) using AJAX
                const request = new XMLHttpRequest();
                request.onreadystatechange = function () {
                  if (this.readyState === 4 && this.status === 200) {
                    console.log(this.response);
                    // If successful, refresh posts
                    updatePosts();
                    // Clear input fields
                    clearInputFields(titleInput, contentInput);
                  } else {
                    console.error("Error uploading image");
                  }
                };
                const postJSONString = JSON.stringify(postJSON);
                request.open("POST", "/add");
                request.setRequestHeader("Content-Type", "application/json");
                request.send(postJSONString);
                clearInputFields(titleInput, contentInput);
                uploadCompleted = false;
              } 
            
            
            
            
            
            
            
            // // Using AJAX
            // const request = new XMLHttpRequest();
            // request.onreadystatechange = function () {
            //     if (this.readyState === 4 && this.status === 200) {
            //         console.log(this.response);
            //         // If successful, refresh posts
            //         updatePosts();
            //         // Clear input fields
            //         clearInputFields(titleInput, contentInput);
            //     }
            // }
            // const postJSON = {"title": title, "content": content};
            // request.open("POST", "/post/add");
            // request.setRequestHeader("Content-Type", "application/json");
            // request.send(JSON.stringify(postJSON));

    
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
    let uploadCompleted=false;
    function uploadFile() {
        const fileInput = document.getElementById("file-upload").files[0];
        if (!fileInput) {
            console.error("No file selected.");
            return;
        }
    
        const formData = new FormData();
        formData.append("file", fileInput);
    
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4) {
                if (this.status === 200) {
                    const response = JSON.parse(this.response);
                    uploadResponse = {success: true,filename: response.filename ? response.filename : null};
                    uploadCompleted=true;
                    console.log("File uploaded successfully");
                } else {
                    uploadResponse = { success: false };
                    console.error("Error uploading file");
                }
            }
        };
        request.open("POST", "/upload");
        request.send(formData);
    }
    
    
    setInterval(updatePosts, 5000);


    const addButton = document.querySelector(".add-post-button");
    addButton.addEventListener("click", function() {
        sendPost();
    });
    

    const uploadButton = document.getElementById("upload-button");
    uploadButton.addEventListener("click", function() {
        uploadFile();
    });

    const darkModeToggle = document.getElementById("dark-mode-toggle");

    darkModeToggle.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
    });

    const gamerModeToggle = document.getElementById("gamer-mode-toggle");

    gamerModeToggle.addEventListener("click", function () {
        document.body.classList.toggle("gamer-mode");
    })

});

