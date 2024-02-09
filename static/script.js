// script.js
document.addEventListener('DOMContentLoaded', function() {
    const recommendBtn = document.getElementById('recommend-btn');
    const movieSelect = document.getElementById('movie-select');
    const recommendationsDiv = document.getElementById('recommendations');

    recommendBtn.addEventListener('click', function() {
        console.log("Clicked")
        const selectedMovie = movieSelect.value;
        fetch('/recommend', {
            method: 'POST',
            body: JSON.stringify({ movie: selectedMovie }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            showRecommendations(data);
        })
        .catch(error => console.error('Error:', error));
    });

    function showRecommendations(recommendations) {
        recommendationsDiv.classList.remove('hidden');
        recommendations.forEach((recommendation, index) => {
            const movieContainer = document.getElementById(`movie${index + 1}`);
            movieContainer.querySelector('.movie-title').textContent = recommendation.name;
            movieContainer.querySelector('.movie-poster').src = recommendation.poster;
        });
    }
});
