/* Part 4 - Simple Web Client - hbnb - Client-side script */

// -----------------------------
// Utility functions
// -----------------------------

// Get cookie value by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// -----------------------------
// Task 2 - Index page functions
// -----------------------------
const mockPlaces = [
    {id: 1, name: "Paris Apartment", description: "Lovely studio in Paris", price: 50},
    {id: 2, name: "NYC Loft", description: "Modern loft in NYC", price: 100},
    {id: 3, name: "Tokyo Condo", description: "Cozy condo in Tokyo", price: 80},
];

// Display places in index.html
function displayPlaces(places) {
    const container = document.getElementById('places-list');
    container.innerHTML = '';
    places.forEach(place => {
        const div = document.createElement('div');
        div.className = 'place-card';
        div.innerHTML = `
            <h3>${place.name}</h3>
            <p>${place.description}</p>
            <p>Price: $${place.price} / night</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        container.appendChild(div);
    });
}

// Check authentication for index.html
function checkAuthenticationIndex() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    if (!loginLink) return; // skip if not on index.html

    if (!token) {
        loginLink.style.display = 'block';
        displayPlaces(mockPlaces); // show mock data if not authenticated
    } else {
        loginLink.style.display = 'none';
        // fetchPlaces(token); // Uncomment if backend API exists
        displayPlaces(mockPlaces);
    }
}

// Filter places by price
function setupPriceFilter() {
    const filter = document.getElementById('price-filter');
    if (!filter) return;

    filter.addEventListener('change', (event) => {
        const value = event.target.value;
        const filtered = mockPlaces.filter(p => !value || p.price <= parseInt(value));
        displayPlaces(filtered);
    });
}

// -----------------------------
// Task 3 - Place Details
// -----------------------------

const mockPlaceDetails = {
    id: 1,
    name: "Paris Apartment",
    description: "Lovely studio in Paris",
    price: 50,
    amenities: ["WiFi", "Air Conditioning", "Kitchen"],
    reviews: [
        {user: "Alice", comment: "Great place!", rating: 5},
        {user: "Bob", comment: "Very comfortable", rating: 4}
    ]
};

// Get place ID from URL
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

// Display place details
function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    if (!container) return;

    container.innerHTML = `
        <h2>${place.name}</h2>
        <p>${place.description}</p>
        <p>Price: $${place.price} / night</p>
        <h3>Amenities:</h3>
        <ul>${place.amenities.map(a => `<li>${a}</li>`).join('')}</ul>
        <h3>Reviews:</h3>
        <div>
            ${place.reviews.map(r => `
                <div class="review-card">
                    <p><strong>${r.user}</strong>: ${r.comment} (Rating: ${r.rating})</p>
                </div>
            `).join('')}
        </div>
    `;
}

// Check authentication for place.html
function checkAuthenticationPlace(placeId) {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    if (!addReviewSection) return;

    if (!token) {
        addReviewSection.style.display = 'none';
        displayPlaceDetails(mockPlaceDetails);
    } else {
        addReviewSection.style.display = 'block';
        // fetchPlaceDetails(token, placeId); // Uncomment if backend API exists
        displayPlaceDetails(mockPlaceDetails);
    }
}

// -----------------------------
// On page load
// -----------------------------
document.addEventListener('DOMContentLoaded', () => {
    checkAuthenticationIndex();
    setupPriceFilter();

    const placeId = getPlaceIdFromURL();
    if (placeId) {
        checkAuthenticationPlace(placeId);
    }
});
