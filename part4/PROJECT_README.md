# Part 4 - HBnB Web Client

A complete front-end web application for the HBnB platform built with HTML5, CSS3, and JavaScript. This web client provides a user-friendly interface to interact with the HBnB RESTful API backend.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Pages Overview](#pages-overview)
- [Testing](#testing)
- [Design Specifications](#design-specifications)
- [API Integration](#api-integration)

---

## Overview

Part 4 is the front-end web client for the HBnB application. It allows users to register, login, browse places, view detailed information about places, and add reviews for places they've visited.

The application uses JWT (JSON Web Tokens) for authentication and communicates with the Part 3 RESTful API backend through a local proxy server to avoid CORS issues.

---

## Features

### Authentication
- **User Registration**: New users can create accounts with email and password
- **User Login**: Existing users can authenticate and receive JWT tokens
- **Session Management**: JWT tokens are stored in cookies for persistent sessions
- **Logout**: Users can logout and clear their session

### Places
- **Browse Places**: View all available places in a responsive grid layout
- **Price Filter**: Filter places by maximum price per night (10, 50, 100, or All)
- **Place Cards**: Each place displays name, price, description, and a "View Details" button

### Place Details
- **Detailed Information**: View comprehensive details including:
  - Place name and description
  - Price per night
  - Host information
  - Amenities list
  - All reviews with ratings
- **Owner Protection**: Place owners cannot review their own places
- **Admin Features**: Admin users can delete places

### Reviews
- **View Reviews**: See all reviews for a place with ratings and comments
- **Add Reviews**: Authenticated users can add reviews to places (except their own)
- **Rating System**: 5-star rating system with visual star display

---

## Project Structure

```
part4/
├── index.html          # Main page - Places listing (requires login)
├── login.html          # Login page (entry point)
├── register.html       # User registration page
├── place.html          # Place details page with reviews
├── add_review.html     # Add review form page
├── scripts.js          # All client-side JavaScript logic
├── styles.css          # Complete styling for all pages
├── server.py           # Local Python server + API proxy
├── HOW_TO_RUN.txt      # Quick start instructions
├── README.md           # Original project documentation
├── PROJECT_README.md   # This file - Complete documentation
└── images/             # Image assets
    ├── logo.png
    ├── place_placeholder.svg
    ├── wifi.png
    ├── bed.png
    └── bathtub.png
```

---

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- Part 3 (API backend) must be set up and running
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Setup Part 3 (API Backend)

```bash
# Navigate to part3 directory
cd part3

# Install dependencies
pip3 install -r requirements.txt

# Reset and initialize database with test data
python3 reset_db.py

# Start the API server
python3 run.py
```

The API will run on `http://127.0.0.1:5000`

**Note**: Keep this terminal window open while using the application.

### Step 2: Start Part 4 (Frontend)

Open a new terminal window:

```bash
# Navigate to part4 directory
cd part4

# Start the frontend server
python3 server.py
```

The frontend will run on `http://127.0.0.1:8000`

**Important**: You MUST use `python3 server.py` (not `python -m http.server`) because the proxy functionality is required to avoid CORS issues.

### Step 3: Access the Application

Open your web browser and navigate to:

```
http://127.0.0.1:8000/
```

You'll be redirected to the login page to begin.

### Default Test Accounts

**Admin Account**:
- Email: `admin@example.com`
- Password: `admin123`

---

## Pages Overview

### 1. Login Page (`login.html`)

**URL**: `http://127.0.0.1:8000/` or `http://127.0.0.1:8000/login.html`

- Entry point for the application
- Email and password form
- Link to registration page
- Automatic redirect to index if already logged in
- Displays error messages for failed login attempts

**Required Elements**:
- Form ID: `login-form`
- Error display: `login-error`
- Email input: `email`
- Password input: `password`

### 2. Registration Page (`register.html`)

**URL**: `http://127.0.0.1:8000/register.html`

- New user registration
- Fields: First Name, Last Name, Email, Password
- Automatic redirect to index after successful registration
- Link back to login page
- Success and error message display

**Required Elements**:
- Form ID: `register-form`
- Error display: `register-error`
- Success display: `register-success`

### 3. Index/Places Page (`index.html`)

**URL**: `http://127.0.0.1:8000/index.html`

- Main page after login
- Displays all places in a responsive grid
- Client-side price filter (no page reload)
- Place cards with name, price, description, and "View Details" button
- Shows/hides login link based on authentication
- Displays admin badge for admin users

**Required Elements**:
- Places container: `places-list`
- Price filter: `price-filter`
- Login link: `login-link`
- Each place card has class: `place-card`
- Details button has class: `details-button`

### 4. Place Details Page (`place.html`)

**URL**: `http://127.0.0.1:8000/place.html?id=PLACE_ID`

- Comprehensive place information
- Host details
- Amenities list
- All reviews displayed as cards
- "Add a Review" link (hidden if user is place owner)
- "Delete Place" button (admin only)

**Required Elements**:
- Place details section: `place-details`
- Place info article: `place-info`
- Add review section: `add-review`
- Each review card has class: `review-card`

### 5. Add Review Page (`add_review.html`)

**URL**: `http://127.0.0.1:8000/add_review.html?place_id=PLACE_ID`

- Form to submit a review
- Rating dropdown (1-5 stars)
- Comment textarea
- Requires authentication (redirects to login if not logged in)
- Success message after submission
- Form reset after successful submission

**Required Elements**:
- Form ID: `add-review-form`
- Message display: `add-review-message`
- Rating select: `rating`
- Comment textarea: `comment`
- Place ID input: `place-id`

---

## Testing

### Manual Testing Checklist

#### Task 0: Design
- [x] All pages have proper header with logo and login button
- [x] All pages have footer with "All rights reserved" text
- [x] Navigation bar present with relevant links
- [x] Place cards have required classes and styling
- [x] Review cards have required classes and styling
- [x] Fixed parameters applied (margin: 20px, padding: 10px, border: 1px solid #ddd, border-radius: 10px)

#### Task 1: Login
- [x] Login form submits via AJAX
- [x] JWT token stored in cookie on success
- [x] Redirect to index.html after successful login
- [x] Error message displayed on login failure
- [x] Link to register page works

#### Task 2: Index
- [x] Login link hidden when user is authenticated
- [x] Places fetched from API and displayed
- [x] Place cards show name, price, and description
- [x] Price filter works without page reload
- [x] Filter options: 10, 50, 100, All
- [x] "View Details" buttons navigate to place.html

#### Task 3: Place Details
- [x] Place ID extracted from URL
- [x] Place details fetched and displayed
- [x] Reviews fetched and displayed
- [x] "Add a Review" link hidden if user is place owner
- [x] Admin users see "Delete Place" button
- [x] All amenities displayed properly

#### Task 4: Add Review
- [x] Authentication checked on page load
- [x] Unauthenticated users redirected to index
- [x] Place ID extracted from URL and displayed
- [x] Form submits review via AJAX
- [x] Success message displayed after submission
- [x] Form cleared after successful submission
- [x] Error messages displayed on failure

### Automated Testing

You can test the API endpoints directly:

```bash
# Test login
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'

# Test fetching places
curl http://127.0.0.1:8000/api/v1/places/

# Test fetching reviews
curl http://127.0.0.1:8000/api/v1/reviews/
```

---

## Design Specifications

### Fixed Parameters (Required)

The following parameters are mandatory per project requirements:

- **Margin**: 20px for place and review cards
- **Padding**: 10px within place and review cards
- **Border**: 1px solid #ddd for place and review cards
- **Border Radius**: 10px for place and review cards

### Flexible Parameters

The following were chosen for the design:

- **Color Palette**:
  - Primary: #333 (Dark gray)
  - Background: #f5f5f5 (Light gray)
  - Accent: #FF5A5F (Red for admin badge)
  - White: #fff for cards and headers

- **Typography**:
  - Font Family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
  - Base Font Size: 16px
  - Line Height: 1.5

- **Images**:
  - Logo: logo.png
  - Place placeholder: place_placeholder.svg
  - Amenity icons: wifi.png, bed.png, bathtub.png

### Required CSS Classes

All required classes are implemented:

- `logo` - Application logo
- `login-button` - Login/logout button styling
- `place-card` - Place listing cards
- `details-button` - View details button
- `place-details` - Place details section container
- `place-info` - Place information article
- `review-card` - Review cards
- `add-review` - Add review section
- `form` - Form styling

---

## API Integration

### Proxy Server

The `server.py` file runs a local server that:
1. Serves static HTML, CSS, JS, and image files
2. Proxies API requests to Part 3 backend
3. Avoids CORS issues by using same-origin requests

### API Endpoints Used

| Method | Endpoint | Purpose | Authentication |
|--------|----------|---------|----------------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | User login | No |
| GET | `/api/v1/places/` | List all places | Optional |
| GET | `/api/v1/places/<id>` | Get place details | Optional |
| DELETE | `/api/v1/places/<id>` | Delete place | Yes (Admin) |
| GET | `/api/v1/reviews/` | List all reviews | No |
| POST | `/api/v1/reviews/` | Create review | Yes |

### Authentication Flow

1. User submits login form
2. Frontend sends POST to `/api/v1/auth/login`
3. Backend validates credentials
4. Backend returns JWT token
5. Frontend stores token in cookie
6. Frontend includes token in Authorization header for protected requests

---

## Troubleshooting

### Common Issues

**Error 404 - Not Found**
- **Cause**: Using `python -m http.server` instead of `python3 server.py`
- **Solution**: Stop the server and start with `python3 server.py`

**Error 502 - Bad Gateway**
- **Cause**: Part 3 (API) is not running
- **Solution**: Start Part 3 with `python3 run.py` from the part3 directory

**Port 5000 Already in Use**
- **Cause**: AirPlay Receiver or another service using port 5000
- **Solution**: Disable AirPlay Receiver in System Settings (macOS) or kill the process using the port

**Login Not Working**
- **Cause**: Database not initialized or wrong credentials
- **Solution**: Run `python3 reset_db.py` from part3 directory to reset database

**Places Not Loading**
- **Cause**: API not running or network error
- **Solution**: Check browser console (F12) for errors, verify both servers are running

---

## W3C Validation

All HTML files should pass W3C HTML validation. To validate:

1. Visit: https://validator.w3.org/
2. Upload or paste your HTML file
3. Check for errors and warnings

All HTML files in this project use:
- Valid HTML5 doctype
- Proper semantic elements
- Required meta tags
- Proper attribute usage

---

## Browser Compatibility

Tested and working on:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Note**: Requires JavaScript enabled and cookie support.

---

## Security Considerations

- JWT tokens stored in cookies with HttpOnly protection
- Passwords never stored in localStorage or visible in console
- CSRF protection through SameSite cookie attribute
- Input sanitization through HTML escaping
- Authentication required for sensitive operations

---

## Future Enhancements

Potential improvements for future versions:
- Image upload for places
- User profile pages
- Edit/delete reviews
- Search and advanced filtering
- Pagination for places and reviews
- Real-time updates using WebSockets
- Mobile app version

---

## Credits

Part of Holberton School HBnB project - A full-stack web application demonstrating modern web development practices.

---

## License

All rights reserved.
