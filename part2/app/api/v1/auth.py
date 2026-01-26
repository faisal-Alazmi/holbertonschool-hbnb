from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.utils.auth import create_token

api = Namespace('auth', description='Authentication operations')

# Define the login model
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return JWT token"""
        data = api.payload or {}
        
        # Validate input
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return {'error': 'Email and password are required'}, 400
        
        # Get user by email
        user = facade.get_user_by_email(email)
        if not user:
            return {'error': 'Invalid credentials'}, 401
        
        # Verify password
        if not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401
        
        # Create token
        token = create_token(user.id)
        
        return {
            'access_token': token,
            'user_id': user.id
        }, 200
