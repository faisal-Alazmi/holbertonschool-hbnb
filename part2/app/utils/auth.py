import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, current_app


def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password, hashed_password):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_token(user_id):
    """Create a JWT token for a user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    secret_key = current_app.config['JWT_SECRET_KEY']
    algorithm = current_app.config['JWT_ALGORITHM']
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode_token(token):
    """Decode and verify a JWT token"""
    try:
        secret_key = current_app.config['JWT_SECRET_KEY']
        algorithm = current_app.config['JWT_ALGORITHM']
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def jwt_required(f):
    """Decorator to require JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Import here to avoid circular import
        from app.services import facade
        
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return {'error': 'Invalid token format'}, 401
        
        if not token:
            return {'error': 'Authentication token is missing'}, 401
        
        # Decode token
        payload = decode_token(token)
        if not payload:
            return {'error': 'Invalid or expired token'}, 401
        
        # Get user from token
        user = facade.get_user(payload['user_id'])
        if not user:
            return {'error': 'User not found'}, 401
        
        # Pass current user to the route
        return f(current_user=user, *args, **kwargs)
    
    return decorated


def get_current_user():
    """Get the current authenticated user from the request token"""
    # Import here to avoid circular import
    from app.services import facade
    
    token = None
    
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return None
    
    if not token:
        return None
    
    payload = decode_token(token)
    if not payload:
        return None
    
    return facade.get_user(payload['user_id'])
