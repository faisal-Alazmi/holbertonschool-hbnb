/* Part 4 - Simple Web Client - hbnb - Client-side scripts */

const API_BASE_URL = 'http://127.0.0.1:5000';

function setTokenCookie(token) {
    const maxAge = 60 * 60 * 24;
    document.cookie = `token=${token}; path=/; max-age=${maxAge}; SameSite=Lax`;
}

function getTokenFromCookie() {
    return getCookie('token');
}

function getCookie(name) {
    const match = document.cookie.match(new RegExp('(?:^|; )' + name.replace(/([.$?*|{}()[\]\\/+^])/g, '\\$1') + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : null;
}

let allPlaces = [];

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const placesList = document.getElementById('places-list');

    if (!loginLink) return;
    if (token) {
        loginLink.style.display = 'none';
        if (placesList) fetchPlaces(token);
    } else {
        loginLink.style.display = 'block';
        if (placesList) placesList.innerHTML = '<p class="page-subtitle">Please log in to see places.</p>';
    }
}

async function fetchPlaces(token) {
    const headers = {};
    if (token) headers['Authorization'] = 'Bearer ' + token;
    const response = await fetch(`${API_BASE_URL}/api/v1/places/`, { headers });
    const data = await response.json().catch(() => []);
    if (response.ok && Array.isArray(data)) {
        allPlaces = data;
        displayPlaces(data);
        attachPriceFilter();
    } else {
        const list = document.getElementById('places-list');
        if (list) list.innerHTML = '<p class="form-error">Could not load places.</p>';
    }
}

function displayPlaces(places) {
    const list = document.getElementById('places-list');
    if (!list) return;
    list.innerHTML = '';
    if (!places.length) {
        list.innerHTML = '<p class="page-subtitle">No places found.</p>';
        return;
    }
    places.forEach((place) => {
        const article = document.createElement('article');
        article.className = 'place-card';
        article.setAttribute('data-id', place.id);
        article.setAttribute('data-price', String(place.price != null ? place.price : ''));
        const title = place.title || 'Unnamed place';
        const price = place.price != null ? place.price : 0;
        const desc = place.description || 'No description.';
        article.innerHTML =
            '<h2>' + escapeHtml(title) + '</h2>' +
            '<p class="price">$' + escapeHtml(String(price)) + ' / night</p>' +
            '<p>' + escapeHtml(desc) + '</p>' +
            '<a href="place.html?id=' + escapeHtml(place.id) + '" class="details-button">View Details</a>';
        list.appendChild(article);
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function applyPriceFilter(maxPrice) {
    const cards = document.querySelectorAll('#places-list .place-card');
    cards.forEach((card) => {
        const price = parseFloat(card.getAttribute('data-price')) || 0;
        const show = maxPrice === '' || price <= maxPrice;
        card.style.display = show ? '' : 'none';
    });
}

function attachPriceFilter() {
    const filter = document.getElementById('price-filter');
    if (!filter) return;
    filter.removeEventListener('change', _onPriceFilterChange);
    filter.addEventListener('change', _onPriceFilterChange);
    _onPriceFilterChange({ target: filter });
}

function _onPriceFilterChange(event) {
    const value = event.target.value;
    const maxPrice = value === '' ? '' : parseFloat(value);
    applyPriceFilter(maxPrice);
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id') || params.get('place_id') || '';
}

async function fetchPlaceDetails(placeId, token) {
    const headers = {};
    if (token) headers['Authorization'] = 'Bearer ' + token;
    const response = await fetch(`${API_BASE_URL}/api/v1/places/${placeId}`, { headers });
    if (!response.ok) return null;
    return response.json().catch(() => null);
}

async function fetchReviewsForPlace(placeId) {
    const response = await fetch(`${API_BASE_URL}/api/v1/reviews/`);
    const data = await response.json().catch(() => []);
    if (!response.ok || !Array.isArray(data)) return [];
    return data.filter((r) => r.place_id === placeId);
}

function displayPlaceDetails(place, reviews) {
    const section = document.getElementById('place-details');
    if (!section) return;
    section.innerHTML = '';

    const title = place.title || 'Unnamed place';
    const price = place.price != null ? place.price : 0;
    const desc = place.description || 'No description.';
    let hostText = 'Hosted by —';
    if (place.owner) {
        const fn = place.owner.first_name || '';
        const ln = place.owner.last_name || '';
        const name = (fn + ' ' + ln).trim() || 'Host';
        hostText = 'Hosted by <strong>' + escapeHtml(name) + '</strong>';
    }
    const amenities = place.amenities || [];
    const amenityNames = amenities.map((a) => (a && a.name) || '').filter(Boolean);

    const grid = document.createElement('div');
    grid.className = 'place-details';
    grid.innerHTML =
        '<div class="place-images">' +
        '<img src="images/sample_place.jpg" alt="Place image">' +
        '</div>' +
        '<article class="place-info">' +
        '<h1>' + escapeHtml(title) + '</h1>' +
        '<p class="host">' + hostText + '</p>' +
        '<p class="price">$' + escapeHtml(String(price)) + ' / night</p>' +
        '<p class="description">' + escapeHtml(desc) + '</p>' +
        '<h2>Amenities</h2>' +
        '<ul class="amenities">' +
        amenityNames.map((n) => '<li>' + escapeHtml(n) + '</li>').join('') +
        '</ul>' +
        '</article>';
    section.appendChild(grid);

    const reviewsSection = document.createElement('section');
    reviewsSection.className = 'reviews-section';
    reviewsSection.innerHTML = '<h2>Reviews</h2>';
    if (reviews.length) {
        reviews.forEach((r) => {
            const card = document.createElement('article');
            card.className = 'review-card';
            let userName = 'Anonymous';
            if (r.user) {
                const fn = r.user.first_name || '';
                const ln = r.user.last_name || '';
                userName = (fn + ' ' + ln).trim() || userName;
            }
            const rating = r.rating != null ? r.rating : 0;
            const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);
            card.innerHTML =
                '<h3>' + escapeHtml(userName) + '</h3>' +
                '<p class="rating">Rating: ' + stars + ' (' + rating + '/5)</p>' +
                '<p class="comment">' + escapeHtml(r.text || '') + '</p>';
            reviewsSection.appendChild(card);
        });
    } else {
        reviewsSection.innerHTML += '<p class="page-subtitle">No reviews yet.</p>';
    }
    section.appendChild(reviewsSection);
}

function initPlacePage() {
    const placeId = getPlaceIdFromURL();
    const section = document.getElementById('place-details');
    const addReviewSection = document.getElementById('add-review');
    const addReviewLink = document.getElementById('add-review-link');
    const token = getCookie('token');

    if (!placeId) {
        if (section) section.innerHTML = '<p class="form-error">Missing place ID.</p>';
        if (addReviewSection) addReviewSection.style.display = 'none';
        return;
    }

    if (addReviewSection) {
        if (token) {
            addReviewSection.style.display = 'block';
            if (addReviewLink) addReviewLink.href = 'add_review.html?place_id=' + encodeURIComponent(placeId);
        } else {
            addReviewSection.style.display = 'none';
        }
    }

    (async () => {
        const place = await fetchPlaceDetails(placeId, token);
        if (!place) {
            if (section) section.innerHTML = '<p class="form-error">Place not found.</p>';
            return;
        }
        const reviews = await fetchReviewsForPlace(placeId);
        displayPlaceDetails(place, reviews);
    })();
}

async function loginUser(email, password) {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json().catch(() => ({}));

    if (response.ok) {
        const token = data.access_token;
        if (token) {
            setTokenCookie(token);
            window.location.href = 'index.html';
        } else {
            return { ok: false, message: 'Invalid response from server' };
        }
    } else {
        const message = data.error || response.statusText || 'Login failed';
        return { ok: false, message };
    }
    return { ok: true };
}

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    if (document.getElementById('place-details')) initPlacePage();

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const emailInput = document.getElementById('email');
            const passwordInput = document.getElementById('password');
            const errorEl = document.getElementById('login-error');

            const email = emailInput ? emailInput.value.trim() : '';
            const password = passwordInput ? passwordInput.value : '';

            if (errorEl) {
                errorEl.style.display = 'none';
                errorEl.textContent = '';
            }

            if (!email || !password) {
                if (errorEl) {
                    errorEl.textContent = 'Please enter email and password.';
                    errorEl.style.display = 'block';
                } else {
                    alert('Please enter email and password.');
                }
                return;
            }

            const submitBtn = loginForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Signing in...';
            }

            try {
                const result = await loginUser(email, password);
                if (!result.ok) {
                    if (errorEl) {
                        errorEl.textContent = result.message;
                        errorEl.style.display = 'block';
                    } else {
                        alert('Login failed: ' + result.message);
                    }
                }
            } catch (err) {
                const msg = err.message || 'Network error. Is the API running?';
                if (errorEl) {
                    errorEl.textContent = msg;
                    errorEl.style.display = 'block';
                } else {
                    alert(msg);
                }
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Login';
                }
            }
        });
    }

    const addReviewForm = document.getElementById('add-review-form');
    if (addReviewForm) {
        const params = new URLSearchParams(window.location.search);
        const placeIdEl = document.getElementById('place-id');
        if (placeIdEl && params.get('place_id')) {
            placeIdEl.value = params.get('place_id');
        }
        addReviewForm.addEventListener('submit', (e) => {
            e.preventDefault();
        });
    }
});
