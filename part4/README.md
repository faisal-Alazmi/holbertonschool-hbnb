# Part 4 - HBnB Web Client

A front-end web application for the HBnB platform built with HTML5, CSS3, and JavaScript. It connects with the RESTful API backend (Part 3) via a local proxy server.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [File Flow & Sequence](#file-flow--sequence)
- [Pages](#pages)
- [Setup Instructions](#setup-instructions)
- [API Integration](#api-integration)
- [Tasks Compliance](#tasks-compliance)

---

## Overview

Part 4 provides a web client that allows users to:

- **Register** – Create new accounts
- **Login** – Authenticate with JWT tokens
- **Browse places** – Grid view with price filter
- **View place details** – Name, description, host, amenities, reviews
- **Add reviews** – Authenticated users (except place owners)
- **Admin features** – Admin badge, delete places

---

## Project Structure

```
part4/
├── index.html          # Places listing page (requires login)
├── login.html          # Login page (first page at /)
├── register.html       # Registration page
├── place.html          # Place details page
├── add_review.html     # Add review form
├── scripts.js         # All client-side logic
├── styles.css         # Styling
├── server.py          # Local server (port 8000) + API proxy to Part 3
├── HOW_TO_RUN.txt     # Quick run instructions
├── images/
│   ├── logo.png       # App logo
│   ├── place_placeholder.svg
│   ├── wifi.png
│   ├── bed.png
│   └── bathtub.png
└── README.md          # This file
```

---

## File Flow & Sequence

### 1. Entry Point

```
User opens http://127.0.0.1:8000/
         │
         ▼
server.py receives "/"
         │
         ▼
Serves login.html (first page)
```

### 2. Authentication Flow

```
login.html
    │
    ├── User submits form → scripts.js (loginUser)
    │       │
    │       ▼
    │   POST /api/v1/auth/login (proxied to Part 3)
    │       │
    │       ▼
    │   Store token in cookie → redirect to index.html
    │
    └── "Create account" link → register.html

register.html
    │
    ├── User submits form → scripts.js (registerUser)
    │       │
    │       ▼
    │   POST /api/v1/auth/register (proxied to Part 3)
    │       │
    │       ▼
    │   Store token in cookie → redirect to index.html
    │
    └── "Sign in" link → login.html
```

### 3. Places Flow

```
index.html
    │
    ├── checkAuthentication() → if no token: redirect to login.html
    │
    └── fetchPlaces()
            │
            ▼
        GET /api/v1/places/ (proxied)
            │
            ▼
        displayPlaces() → fills #places-list with place cards
            │
            ▼
        Each card: "View Details" → place.html?id=<place_id>
```

### 4. Place Details Flow

```
place.html?id=xxx
    │
    ├── initPlacePage()
    │       │
    │       ├── fetchPlaceDetails(placeId) → GET /api/v1/places/<id>
    │       ├── fetchReviewsForPlace(placeId) → GET /api/v1/reviews/ (filter by place_id)
    │       ├── displayPlaceDetails()
    │       │
    │       ├── If user = place owner → hide "Add a Review"
    │       └── If user = admin → show "Delete Place" button
    │
    └── "Add a Review" link → add_review.html?place_id=xxx
```

### 5. Add Review Flow

```
add_review.html?place_id=xxx
    │
    ├── checkAuthForAddReview() → if no token: redirect to login.html
    │
    └── Form submit → submitReview()
            │
            ▼
        POST /api/v1/reviews/
        Body: { text, rating, user_id (from token), place_id }
            │
            ▼
        Success → show message, reset form
```

### 6. Proxy Flow

```
Browser                    server.py (8000)              Part 3 (5000)
   │                            │                              │
   │  GET /api/v1/places/       │                              │
   ├───────────────────────────>│  GET http://127.0.0.1:5000/  │
   │                            │  api/v1/places/              │
   │                            ├─────────────────────────────>│
   │                            │                              │
   │                            │  JSON response               │
   │                            │<─────────────────────────────┤
   │  JSON response             │                              │
   │<───────────────────────────┤                              │
```

---

## Pages

| Page | Purpose | Key IDs |
|------|---------|---------|
| [index.html](index.html) | Places listing with price filter | `places-list`, `price-filter`, `login-link` |
| [login.html](login.html) | Login form | `login-form`, `login-error` |
| [register.html](register.html) | Registration form | `register-form`, `register-error` |
| [place.html](place.html) | Place details + reviews | `place-details`, `add-review` |
| [add_review.html](add_review.html) | Add review form | `add-review-form`, `add-review-message` |

---

## Setup Instructions

### Prerequisites

- Python 3.7+
- Part 3 (API) running on port 5000

### Step 1: Start Part 3 (API)

```bash
cd part3
pip install -r requirements.txt
python run.py
```

→ API runs on `http://127.0.0.1:5000`

### Step 2: Start Part 4 (Frontend)

```bash
cd part4
python server.py
```

→ Frontend runs on `http://127.0.0.1:8000`

**Important:** Use `python server.py`, NOT `python -m http.server 8000` (the proxy is required).

### Step 3: Open Browser

```
http://127.0.0.1:8000/
```

Login page appears first. After login → Places page.

### Default Admin

- **Email:** `admin@example.com`
- **Password:** `admin123`

(Run `python reset_db.py` from part3 if needed to reset the database.)

---

## API Integration

All API calls go through the proxy (same origin), so no CORS setup is needed.

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login |
| GET | `/api/v1/places/` | List places |
| GET | `/api/v1/places/<id>` | Place details |
| DELETE | `/api/v1/places/<id>` | Delete place (admin only) |
| GET | `/api/v1/reviews/` | List all reviews |
| POST | `/api/v1/reviews/` | Add review |

---

## Tasks Compliance

### Task 0: Design ✅
- Required classes: `logo`, `login-button`, `place-card`, `details-button`, `place-details`, `place-info`, `review-card`, `add-review`, `form`
- Fixed: margin 20px, padding 10px, border 1px solid #ddd, border-radius 10px

### Task 1: Login ✅
- Form with email, password
- JWT in cookie, redirect after login
- Error display on failure

### Task 2: Index ✅
- `places-list`, `price-filter`, `login-link`
- Fetches places from API, client-side price filter

### Task 3: Place Details ✅
- `place-details`, `add-review`
- Place ID from URL, fetch details & reviews
- Hide add review if user is owner

### Task 4: Add Review ✅
- Form with rating and comment
- Auth required, place_id from URL
- POST to /api/v1/reviews/

---

**Part of Holberton School HBnB project**
