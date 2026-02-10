/* Part 4 - Simple Web Client - hbnb - Client-side scripts */

document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();
        });
    }

    const addReviewForm = document.getElementById('add-review-form');
    if (addReviewForm) {
        const params = new URLSearchParams(window.location.search);
        const placeId = document.getElementById('place-id');
        if (placeId && params.get('place_id')) {
            placeId.value = params.get('place_id');
        }
        addReviewForm.addEventListener('submit', function (e) {
            e.preventDefault();
        });
    }
});
