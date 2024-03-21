document.addEventListener("DOMContentLoaded", function() {
    // Function to send post data to the server
    function sendPostData(title, content) {
        const postData = {
            title: title,
            content: content
        };

        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4) {
                if (this.status === 200) {
                    console.log("Post added successfully:", this.response);
                    fetchAndDisplayPosts(); // Update posts after adding
                } else {
                    console.error("Failed to add post:", this.response);
                }
            }
        };

        request.open("POST", "/post/add");
        request.setRequestHeader("Content-Type", "application/json");
        request.send(JSON.stringify(postData));
    }

    // Function to fetch and display posts
    function fetchAndDisplayPosts() {
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4) {
                if (this.status === 200) {
                    const posts = JSON.parse(this.response);
                    displayPosts(posts);
                } else {
                    console.error("Failed to fetch posts:", this.response);
                }
            }
        };

        request.open("GET", "../static/TestingPosts/Test_posts.json");
        request.send();
    }

    // Function to display posts
    function displayPosts(posts) {
        const postsContainer = document.getElementById("posts-container");
        postsContainer.innerHTML = ""; // Clear existing posts

        posts.forEach(post => {
            const postElement = document.createElement("div");
            postElement.classList.add("post");

            const headerElement = document.createElement("div");
            headerElement.classList.add("header");

            const usernameTitleElement = document.createElement("p");
            usernameTitleElement.classList.add("username-title");
            usernameTitleElement.textContent = post.username + ": " + post.title;

            const contentElement = document.createElement("p");
            contentElement.classList.add("content");
            contentElement.textContent = post.content;

            headerElement.appendChild(usernameTitleElement);
            postElement.appendChild(headerElement);
            postElement.appendChild(contentElement);

            postsContainer.appendChild(postElement);
        });
    }

    // Event listener for Add Post button
    const addButton = document.querySelector(".add-post-button");
    addButton.addEventListener("click", function() {
        const titleInput = document.querySelector(".post-title-input");
        const contentInput = document.querySelector(".post-content-input");
        const title = titleInput.value.trim();
        const content = contentInput.value.trim();
        
        // Check if both title and content are provided
        if (title !== "" && content !== "") {
            sendPostData(title, content);
            
            // Clear input boxes after submitting post
            titleInput.value = "";
            contentInput.value = "";
        } else {
            console.error("Please provide both title and content for the post.");
        }
    });

    // Fetch and display posts when the page loads
    fetchAndDisplayPosts();
});

