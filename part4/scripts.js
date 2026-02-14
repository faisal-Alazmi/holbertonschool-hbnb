/* Part 4 - Simple Web Client - hbnb - Client-side scripts */

// Use same origin so Part 4 server (server.py) can proxy to Part 3 – avoids CORS
const API_BASE_URL = '';

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

function logout() {
    document.cookie = 'token=; path=/; max-age=0';
    window.location.href = 'login.html';
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    const adminBadge = document.getElementById('admin-badge');
    const placesList = document.getElementById('places-list');

    if (loginLink) loginLink.style.display = token ? 'none' : 'block';
    if (logoutLink) logoutLink.style.display = token ? 'block' : 'none';
    if (adminBadge) adminBadge.style.display = (token && isAdmin()) ? 'inline-block' : 'none';

    if (token) {
        if (placesList) {
            placesList.innerHTML = '<p class="page-subtitle">Loading places...</p>';
            fetchPlaces(token);
        }
    } else {
        if (placesList) {
            window.location.href = 'login.html';
            return;
        }
    }
}

function _apiErrorMessage(list, status, body) {
    if (!list) return;
    let msg = 'Could not load places.';
    if (status === 404) {
        msg = 'API path not found. Use Part 4 server: run python server.py from part4 folder (not python -m http.server).';
    } else if (status === 502 || status === 0) {
        msg = 'Part 3 (API) is not running. From part3 folder run: python run.py and keep the terminal open.';
    } else if (status) {
        msg = 'Server error: ' + status + (body ? ' — ' + body : '');
    }
    list.innerHTML = '<p class="form-error">' + msg + '</p>';
}

async function fetchPlaces(token) {
    const list = document.getElementById('places-list');
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/places/`);
        const text = await response.text();
        let data = [];
        try { data = JSON.parse(text); } catch (_) {}
        if (response.ok && Array.isArray(data)) {
            allPlaces = data;
            displayPlaces(data);
            attachPriceFilter();
        } else {
            _apiErrorMessage(list, response.status, text.slice(0, 80));
        }
    } catch (err) {
        console.error('fetchPlaces failed:', err);
        _apiErrorMessage(list, 0, err.message || 'Check F12 → Console for details.');
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
            '<div class="place-card-img"><img src="images/place_placeholder.svg" alt="' + escapeHtml(title) + '"></div>' +
            '<div class="place-card-body">' +
            '<h2>' + escapeHtml(title) + '</h2>' +
            '<p class="price">$' + escapeHtml(String(price)) + ' / night</p>' +
            '<p>' + escapeHtml(desc) + '</p>' +
            '<a href="place.html?id=' + escapeHtml(place.id) + '" class="details-button">View Details</a>' +
            '</div>';
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

function getUserIdFromToken(token) {
    if (!token) return null;
    try {
        const payload = token.split('.')[1];
        if (!payload) return null;
        const decoded = JSON.parse(atob(payload));
        return decoded.sub || null;
    } catch (e) {
        return null;
    }
}

function isAdmin() {
    const token = getCookie('token');
    if (!token) return false;
    try {
        const payload = token.split('.')[1];
        if (!payload) return false;
        const decoded = JSON.parse(atob(payload));
        return decoded.is_admin === true;
    } catch (e) {
        return false;
    }
}

async function registerUser(firstName, lastName, email, password) {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password
        })
    });
    const data = await response.json().catch(() => ({}));
    if (response.ok && data.access_token) {
        setTokenCookie(data.access_token);
        return { ok: true };
    }
    return { ok: false, message: data.error || response.statusText || 'Registration failed' };
}

function checkAuthForAddReview() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'login.html';
        return null;
    }
    return token;
}

async function submitReview(token, placeId, text, rating) {
    const userId = getUserIdFromToken(token);
    if (!userId) return { ok: false, message: 'Invalid session.' };
    const response = await fetch(`${API_BASE_URL}/api/v1/reviews/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify({
            text: text,
            rating: parseInt(rating, 10),
            user_id: userId,
            place_id: placeId
        })
    });
    const data = await response.json().catch(() => ({}));
    if (response.ok) return { ok: true };
    return { ok: false, message: data.error || response.statusText || 'Failed to submit review' };
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
        '<img src="images/place_placeholder.svg" alt="' + escapeHtml(title) + '">' +
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
        '<button id="delete-place-btn" type="button" class="delete-button" style="display:none; margin-top:12px;">Delete Place (Admin)</button>' +
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

async function deletePlace(placeId, token) {
    if (!confirm('Delete this place?')) return;
    const response = await fetch(`${API_BASE_URL}/api/v1/places/${placeId}`, {
        method: 'DELETE',
        headers: { 'Authorization': 'Bearer ' + token }
    });
    if (response.ok) {
        window.location.href = 'index.html';
    } else {
        const data = await response.json().catch(() => ({}));
        alert(data.error || 'Failed to delete place.');
    }
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

    (async () => {
        const place = await fetchPlaceDetails(placeId, token);
        if (!place) {
            if (section) section.innerHTML = '<p class="form-error">Place not found.</p>';
            return;
        }
        const reviews = await fetchReviewsForPlace(placeId);
        displayPlaceDetails(place, reviews);

        const currentUserId = token ? getUserIdFromToken(token) : null;
        const isOwner = place.owner_id && currentUserId && String(place.owner_id) === String(currentUserId);

        if (addReviewSection) {
            if (token && !isOwner) {
                addReviewSection.style.display = 'block';
                if (addReviewLink) addReviewLink.href = 'add_review.html?place_id=' + encodeURIComponent(placeId);
            } else {
                addReviewSection.style.display = 'none';
            }
        }

        if (token && isAdmin()) {
            const deleteBtn = document.getElementById('delete-place-btn');
            if (deleteBtn) {
                deleteBtn.style.display = 'inline-block';
                deleteBtn.onclick = () => deletePlace(placeId, token);
            }
        }
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
            return { ok: true };
        }
        return { ok: false, message: 'Invalid response from server' };
    } else {
        const message = data.error || response.statusText || 'Login failed';
        return { ok: false, message };
    }
}

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) logoutLink.addEventListener('click', function (e) { e.preventDefault(); logout(); });
    if (document.getElementById('place-details')) initPlacePage();

    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const firstName = document.getElementById('firstName')?.value.trim() || '';
            const lastName = document.getElementById('lastName')?.value.trim() || '';
            const email = document.getElementById('reg-email')?.value.trim() || '';
            const password = document.getElementById('reg-password')?.value || '';
            const errorEl = document.getElementById('register-error');
            const successEl = document.getElementById('register-success');
            const submitBtn = registerForm.querySelector('button[type="submit"]');

            if (errorEl) { errorEl.style.display = 'none'; errorEl.textContent = ''; }
            if (successEl) successEl.style.display = 'none';

            if (!firstName || !lastName || !email || !password) {
                if (errorEl) { errorEl.textContent = 'Please fill all fields.'; errorEl.style.display = 'block'; }
                return;
            }

            if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Creating...'; }

            try {
                const result = await registerUser(firstName, lastName, email, password);
                if (result.ok) {
                    if (successEl) { successEl.textContent = 'Account created! Redirecting...'; successEl.style.display = 'block'; }
                    setTimeout(() => { window.location.href = 'index.html'; }, 800);
                } else {
                    if (errorEl) { errorEl.textContent = result.message; errorEl.style.display = 'block'; }
                }
            } catch (err) {
                if (errorEl) { errorEl.textContent = err.message || 'Registration failed.'; errorEl.style.display = 'block'; }
            }
            if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Create Account'; }
        });
    }

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
        const token = checkAuthForAddReview();
        if (!token) return;

        const placeId = getPlaceIdFromURL();
        const placeIdEl = document.getElementById('place-id');
        if (placeIdEl) placeIdEl.value = placeId || '';
        if (!placeId) {
            window.location.href = 'index.html';
            return;
        }

        addReviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const messageEl = document.getElementById('add-review-message');
            const ratingEl = document.getElementById('rating');
            const commentEl = document.getElementById('comment');
            const rating = ratingEl ? ratingEl.value : '';
            const text = commentEl ? commentEl.value.trim() : '';

            if (messageEl) {
                messageEl.style.display = 'none';
                messageEl.textContent = '';
                messageEl.classList.remove('form-success');
            }

            if (!rating || !text) {
                if (messageEl) {
                    messageEl.textContent = 'Please select a rating and enter your comment.';
                    messageEl.style.display = 'block';
                } else alert('Please select a rating and enter your comment.');
                return;
            }

            const submitBtn = addReviewForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Submitting...';
            }

            try {
                const result = await submitReview(token, placeId, text, rating);
                if (result.ok) {
                    if (messageEl) {
                        messageEl.textContent = 'Review submitted successfully!';
                        messageEl.classList.add('form-success');
                        messageEl.style.display = 'block';
                    } else alert('Review submitted successfully!');
                    addReviewForm.reset();
                    if (placeIdEl) placeIdEl.value = placeId;
                } else {
                    if (messageEl) {
                        messageEl.textContent = result.message || 'Failed to submit review.';
                        messageEl.style.display = 'block';
                    } else alert(result.message || 'Failed to submit review.');
                }
            } catch (err) {
                const msg = err.message || 'Network error.';
                if (messageEl) {
                    messageEl.textContent = msg;
                    messageEl.style.display = 'block';
                } else alert(msg);
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Submit Review';
                }
            }
        });
    }
});
