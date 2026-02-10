/* Part 4 - Simple Web Client - hbnb - Client-side scripts */

const API_BASE_URL = 'http://127.0.0.1:5000';

function setTokenCookie(token) {
    const maxAge = 60 * 60 * 24;
    document.cookie = `token=${token}; path=/; max-age=${maxAge}; SameSite=Lax`;
}

function getTokenFromCookie() {
    const match = document.cookie.match(/token=([^;]+)/);
    return match ? match[1] : null;
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
