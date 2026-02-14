from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

register_model = api.model('Register', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})


@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        data = api.payload or {}
        required = ['first_name', 'last_name', 'email', 'password']
        missing = [f for f in required if not data.get(f)]
        if missing:
            return {'error': f"Missing: {', '.join(missing)}"}, 400
        if facade.get_user_by_email(data.get('email')):
            return {'error': 'Email already exists'}, 400
        try:
            user = facade.create_user(data)
            token = create_access_token(
                identity=str(user.id),
                additional_claims={"is_admin": user.is_admin}
            )
            return {'access_token': token}, 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        credentials = api.payload or {}
        email = credentials.get('email')
        password = credentials.get('password')

        if not email or not password:
            return {'error': 'Missing email or password'}, 400

        user = facade.get_user_by_email(email)

        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )
        
        return {'access_token': access_token}, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        return {
            'message': f'Hello, user {current_user}',
            'is_admin': is_admin
        }, 200
