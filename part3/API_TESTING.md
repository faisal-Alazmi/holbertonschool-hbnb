# HBnB API Testing Guide

Complete guide for testing the HBnB API using cURL, Postman, and Python requests.

## Table of Contents
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [User Endpoints](#user-endpoints)
- [Amenity Endpoints](#amenity-endpoints)
- [Place Endpoints](#place-endpoints)
- [Review Endpoints](#review-endpoints)
- [Testing Tools](#testing-tools)

---

## Getting Started

### Start the Server

```bash
cd part3
python3 run.py
```

Server will be available at: `http://127.0.0.1:5000`

### API Documentation

Swagger UI: `http://127.0.0.1:5000/api/v1/`

### Default Admin Credentials

```
Email: admin@example.com
Password: admin123
```

---

## Authentication

### Login to Get JWT Token

#### cURL
```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

#### Expected Response
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Save Token for Later Use
```bash
# Set token as environment variable
export TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."

# Or save to file
echo "eyJ0eXAiOiJKV1QiLCJhbGc..." > token.txt
TOKEN=$(cat token.txt)
```

### Test Invalid Login

```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "wrongpassword"
  }'
```

**Expected**: 401 Unauthorized

---

## User Endpoints

### Create User (Admin Only)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "password123"
  }'
```

**Expected**: 201 Created

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "is_admin": false,
  "created_at": "2026-01-31T10:00:00",
  "updated_at": "2026-01-31T10:00:00"
}
```

### List All Users (Admin Only)

```bash
curl -X GET http://127.0.0.1:5000/api/v1/users/ \
  -H "Authorization: Bearer $TOKEN"
```

### Get User by ID

```bash
USER_ID="550e8400-e29b-41d4-a716-446655440000"

curl -X GET http://127.0.0.1:5000/api/v1/users/$USER_ID \
  -H "Authorization: Bearer $TOKEN"
```

### Update User

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/users/$USER_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "first_name": "Jane"
  }'
```

**Note**: Users can only update their own profile unless they are admin.

### Test Unauthorized Access

```bash
# Try to create user without token
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Expected**: 401 Unauthorized

---

## Amenity Endpoints

### Create Amenity (Admin Only)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "WiFi"
  }'
```

**Expected**: 201 Created

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "WiFi",
  "created_at": "2026-01-31T10:00:00",
  "updated_at": "2026-01-31T10:00:00"
}
```

### List All Amenities (Public)

```bash
# No authentication required
curl -X GET http://127.0.0.1:5000/api/v1/amenities/
```

### Get Amenity by ID (Public)

```bash
AMENITY_ID="a1b2c3d4-e5f6-7890-abcd-ef1234567890"

curl -X GET http://127.0.0.1:5000/api/v1/amenities/$AMENITY_ID
```

### Update Amenity (Admin Only)

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/$AMENITY_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "High-Speed WiFi"
  }'
```

### Delete Amenity (Admin Only)

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/amenities/$AMENITY_ID \
  -H "Authorization: Bearer $TOKEN"
```

**Expected**: 204 No Content

---

## Place Endpoints

### Create Place (Authenticated Users)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Cozy Apartment in Downtown",
    "description": "A beautiful 2-bedroom apartment with city views",
    "price": 120.50,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "owner_id": "550e8400-e29b-41d4-a716-446655440000",
    "amenities": ["a1b2c3d4-e5f6-7890-abcd-ef1234567890"]
  }'
```

**Expected**: 201 Created

```json
{
  "id": "p1a2c3e4-5678-90ab-cdef-123456789012",
  "title": "Cozy Apartment in Downtown",
  "description": "A beautiful 2-bedroom apartment with city views",
  "price": 120.5,
  "latitude": 40.7128,
  "longitude": -74.006,
  "owner_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-01-31T10:00:00",
  "updated_at": "2026-01-31T10:00:00"
}
```

### List All Places (Public)

```bash
curl -X GET http://127.0.0.1:5000/api/v1/places/
```

### Get Place by ID (Public)

```bash
PLACE_ID="p1a2c3e4-5678-90ab-cdef-123456789012"

curl -X GET http://127.0.0.1:5000/api/v1/places/$PLACE_ID
```

### Update Place (Owner or Admin Only)

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/places/$PLACE_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Updated Apartment Title",
    "price": 150.00
  }'
```

**Note**: Only the place owner or admin can update.

### Delete Place (Owner or Admin Only)

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/places/$PLACE_ID \
  -H "Authorization: Bearer $TOKEN"
```

**Expected**: 204 No Content

### Test Non-Owner Update

```bash
# Login as different user
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "other@example.com",
    "password": "password123"
  }'

# Try to update place owned by someone else
curl -X PUT http://127.0.0.1:5000/api/v1/places/$PLACE_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OTHER_TOKEN" \
  -d '{
    "title": "Hacked Title"
  }'
```

**Expected**: 403 Forbidden

---

## Review Endpoints

### Create Review (Authenticated Users)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Amazing place! Very clean and comfortable.",
    "rating": 5,
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "place_id": "p1a2c3e4-5678-90ab-cdef-123456789012"
  }'
```

**Expected**: 201 Created

```json
{
  "id": "r1e2v3i4-5678-90ab-cdef-123456789012",
  "text": "Amazing place! Very clean and comfortable.",
  "rating": 5,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "place_id": "p1a2c3e4-5678-90ab-cdef-123456789012",
  "created_at": "2026-01-31T10:00:00",
  "updated_at": "2026-01-31T10:00:00"
}
```

### List All Reviews (Public)

```bash
curl -X GET http://127.0.0.1:5000/api/v1/reviews/
```

### Get Review by ID (Public)

```bash
REVIEW_ID="r1e2v3i4-5678-90ab-cdef-123456789012"

curl -X GET http://127.0.0.1:5000/api/v1/reviews/$REVIEW_ID
```

### Update Review (Author or Admin Only)

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/reviews/$REVIEW_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Updated review text",
    "rating": 4
  }'
```

### Delete Review (Author or Admin Only)

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/$REVIEW_ID \
  -H "Authorization: Bearer $TOKEN"
```

**Expected**: 204 No Content

### Test Rating Validation

```bash
# Invalid rating (must be 1-5)
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "Test review",
    "rating": 6,
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "place_id": "p1a2c3e4-5678-90ab-cdef-123456789012"
  }'
```

**Expected**: 400 Bad Request

---

## Testing Tools

### Using Postman

1. **Import API Collection**
   - Open Postman
   - Import from URL: `http://127.0.0.1:5000/api/v1/`

2. **Set Up Environment**
   ```
   Variable: BASE_URL
   Value: http://127.0.0.1:5000/api/v1

   Variable: TOKEN
   Value: (paste your JWT token here)
   ```

3. **Use in Requests**
   ```
   URL: {{BASE_URL}}/users/
   Headers: Authorization: Bearer {{TOKEN}}
   ```

### Using Python Requests

```python
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "admin@example.com",
    "password": "admin123"
})
token = response.json()["access_token"]

# Headers for authenticated requests
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Create user
response = requests.post(f"{BASE_URL}/users/",
    headers=headers,
    json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "password123"
    }
)
print(response.status_code)
print(response.json())

# List users
response = requests.get(f"{BASE_URL}/users/", headers=headers)
users = response.json()
print(f"Total users: {len(users)}")
```

### Using HTTPie (Alternative to cURL)

```bash
# Install
pip install httpie

# Login
http POST http://127.0.0.1:5000/api/v1/auth/login \
  email="admin@example.com" \
  password="admin123"

# Create user
http POST http://127.0.0.1:5000/api/v1/users/ \
  Authorization:"Bearer $TOKEN" \
  first_name="John" \
  last_name="Doe" \
  email="john@example.com" \
  password="password123"

# List users
http GET http://127.0.0.1:5000/api/v1/users/ \
  Authorization:"Bearer $TOKEN"
```

---

## Complete Test Workflow

### 1. Setup

```bash
# Start server
python3 run.py

# In another terminal, login
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}' \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

echo "Token: $TOKEN"
```

### 2. Create Test Data

```bash
# Create amenities
WIFI_ID=$(curl -s -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "WiFi"}' \
  | grep -o '"id":"[^"]*' | cut -d'"' -f4)

POOL_ID=$(curl -s -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "Swimming Pool"}' \
  | grep -o '"id":"[^"]*' | cut -d'"' -f4)

# Create user
USER_ID=$(curl -s -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "password123"
  }' \
  | grep -o '"id":"[^"]*' | cut -d'"' -f4)

# Login as new user
USER_TOKEN=$(curl -s -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "password123"}' \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

# Create place
PLACE_ID=$(curl -s -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d "{
    \"title\": \"Cozy Apartment\",
    \"description\": \"Nice place\",
    \"price\": 100.0,
    \"latitude\": 40.7128,
    \"longitude\": -74.0060,
    \"owner_id\": \"$USER_ID\",
    \"amenities\": [\"$WIFI_ID\", \"$POOL_ID\"]
  }" \
  | grep -o '"id":"[^"]*' | cut -d'"' -f4)

# Create review
REVIEW_ID=$(curl -s -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"text\": \"Great place!\",
    \"rating\": 5,
    \"user_id\": \"$USER_ID\",
    \"place_id\": \"$PLACE_ID\"
  }" \
  | grep -o '"id":"[^"]*' | cut -d'"' -f4)

echo "Setup complete!"
echo "User ID: $USER_ID"
echo "Place ID: $PLACE_ID"
echo "Review ID: $REVIEW_ID"
```

### 3. Verify Data

```bash
# List all places
curl -X GET http://127.0.0.1:5000/api/v1/places/

# Get specific place
curl -X GET http://127.0.0.1:5000/api/v1/places/$PLACE_ID

# List all reviews
curl -X GET http://127.0.0.1:5000/api/v1/reviews/
```

### 4. Test Authorization

```bash
# Try to update place as admin (should succeed)
curl -X PUT http://127.0.0.1:5000/api/v1/places/$PLACE_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"price": 150.0}'

# Try to delete place without auth (should fail)
curl -X DELETE http://127.0.0.1:5000/api/v1/places/$PLACE_ID
```

---

## Common HTTP Status Codes

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Successful GET, PUT |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid data |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource |
| 500 | Server Error | Internal server error |

---

## Troubleshooting

### Token Expired
```bash
# Get new token
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}' \
  | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
```

### Pretty Print JSON
```bash
# Add | jq to the end of curl commands
curl -X GET http://127.0.0.1:5000/api/v1/places/ | jq
```

### Debug Mode
```bash
# Add -v for verbose output
curl -v -X GET http://127.0.0.1:5000/api/v1/places/
```

---

**Last Updated**: 2026
**API Version**: v1
**Base URL**: `http://127.0.0.1:5000/api/v1`
