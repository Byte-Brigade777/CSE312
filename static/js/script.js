document.addEventListener("DOMContentLoaded", function() {
    fetch("../static/TestingPosts/Test_posts.json")
        .then(response => response.json())
        .then(posts => {
            const postsContainer = document.getElementById("posts-container");

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
        })
        .catch(error => console.error("Error fetching posts:", error));
});