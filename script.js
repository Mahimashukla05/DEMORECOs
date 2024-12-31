const searchButton = document.getElementById("search-button");
const searchInput = document.getElementById("search-input");
const moviesGrid = document.getElementById("movies-grid");

searchButton.addEventListener("click", () => {
    const query = searchInput.value.trim();

    if (query) {
        fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query }),
        })
            .then((response) => response.json())
            .then((data) => {
                // Clear previous results
                moviesGrid.innerHTML = "";

                if (data.movies.length > 0) {
                    // Display new movie recommendations
                    data.movies.forEach((movie) => {
                        const movieBox = document.createElement("div");
                        movieBox.classList.add("movie-box");
                        movieBox.innerHTML = `<h3>${movie}</h3>`;
                        moviesGrid.appendChild(movieBox);
                    });
                } else {
                    moviesGrid.innerHTML = "<p>No movies found</p>";
                }
            })
            .catch((error) => console.error("Error fetching movies:", error));
    }
});
