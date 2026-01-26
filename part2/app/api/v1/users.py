# app/api/v1/users.py
from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.utils.auth import jwt_required

api = Namespace("users", description="User operations")

# Output model
user_model = api.model("User", {
    "id": fields.String(readonly=True),
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "created_at": fields.String,
    "updated_at": fields.String
})

# Input model
user_input = api.model("UserInput", {
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})

@api.route("/")
class UserList(Resource):
    @api.expect(user_input)
    @api.marshal_with(user_model, code=201)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        data = api.payload
        # Validation
        required_fields = ["first_name", "last_name", "email", "password"]
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            api.abort(400, f"Missing required field(s): {', '.join(missing)}")
        user = facade.create_user(data)
        return user.to_dict(), 201
    
    @api.marshal_list_with(user_model)
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        return [u.to_dict() for u in users], 200

@api.route("/<string:user_id>")
class UserResource(Resource):
    @api.marshal_with(user_model)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get a specific user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict()
    
    @api.expect(user_input)
    @api.response(200, 'User updated successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden - can only update own profile')
    @api.response(404, 'User not found')
    @jwt_required
    def put(self, current_user, user_id):
        """Update user information (requires authentication, users can only update their own profile)"""
        # Check if user is trying to update their own profile
        if current_user.id != user_id:
            api.abort(403, 'You can only update your own profile')
        
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        data = api.payload
        user = facade.update_user(user_id, data)
        return user.to_dict()
