from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Login model
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return JWT token"""
        credentials = api.payload or {}
        email = credentials.get('email')
        password = credentials.get('password')

        if not email or not password:
            return {'error': 'Missing email or password'}, 400

        # Get user by email
        user = facade.get_user_by_email(email)

        # Verify credentials
        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401
        
        # Create JWT token
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )
        
        return {'access_token': access_token}, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """Protected endpoint example"""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        return {
            'message': f'Hello, user {current_user}',
            'is_admin': is_admin
        }, 200
