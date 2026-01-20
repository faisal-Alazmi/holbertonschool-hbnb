# JWT Authentication Implementation

## Overview
This document describes the JWT-based authentication implementation for the HBnB application in the part3 directory.

## Features Implemented

### 1. User Model Enhancements
- **Password Hashing**: Passwords are hashed using bcrypt before storage
- **Password Verification**: Secure password verification method
- **Admin Flag**: Support for admin users with `is_admin` attribute
- **Location**: `part3/app/models/user.py`

### 2. JWT Configuration
- **JWT Manager**: Initialized in Flask application
- **Secret Key**: Configured in config.py with JWT_SECRET_KEY
- **Bcrypt Integration**: Password hashing enabled application-wide
- **Location**: `part3/app/__init__.py` and `part3/config.py`

### 3. Authentication Endpoints

#### Login Endpoint
- **URL**: `POST /api/v1/auth/login`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response (Success)**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
- **Response (Error)**:
  ```json
  {
    "error": "Invalid credentials"
  }
  ```

#### Protected Endpoint
- **URL**: `GET /api/v1/auth/protected`
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
  ```json
  {
    "message": "Hello, user <user_id>",
    "is_admin": false
  }
  ```

### 4. Facade Enhancements
- **get_user_by_email**: Method to retrieve users by email address
- **is_admin Support**: User creation now supports is_admin parameter
- **Location**: `part3/app/services/facade.py`

## Security Features

1. **Password Security**
   - Passwords are hashed with bcrypt before storage
   - Plain text passwords are never stored
   - Password verification uses secure comparison

2. **JWT Token Security**
   - Tokens are signed with SECRET_KEY
   - Tokens include user ID and is_admin claim
   - Token expiration is handled by flask-jwt-extended

3. **Authentication Protection**
   - Invalid credentials return 401 without leaking information
   - Missing tokens are properly rejected
   - Protected endpoints require valid JWT tokens

## Testing Results

All tests passed successfully:
- ✅ Regular user creation and login
- ✅ Admin user creation and login
- ✅ Protected endpoint with valid token
- ✅ Invalid credentials handling (401 error)
- ✅ Missing authorization header handling

## Dependencies Added

```txt
flask-jwt-extended
flask-bcrypt
```

## Usage Examples

### Creating a User
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "securePassword123"
}'
```

### Logging In
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
-H "Content-Type: application/json" \
-d '{
  "email": "john.doe@example.com",
  "password": "securePassword123"
}'
```

### Accessing Protected Endpoint
```bash
curl -X GET "http://127.0.0.1:5000/api/v1/auth/protected" \
-H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Files Modified/Created

1. **Created**: `part3/app/api/v1/auth.py` - Authentication endpoints
2. **Modified**: `part3/requirements.txt` - Added JWT and bcrypt dependencies
3. **Modified**: `part3/app/models/user.py` - Password hashing and verification
4. **Modified**: `part3/app/__init__.py` - JWT and bcrypt initialization
5. **Modified**: `part3/config.py` - JWT configuration
6. **Modified**: `part3/app/services/facade.py` - User lookup by email
7. **Modified**: `part3/app/api/v1/__init__.py` - Auth namespace registration

## Notes

- All changes are isolated to the part3 directory
- Backward compatibility maintained with existing functionality
- Code follows existing project conventions and patterns
- Implementation matches all requirements from the problem statement
