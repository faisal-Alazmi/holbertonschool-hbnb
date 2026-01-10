from flask_restx import Namespace, Resource, fields
from app.services import facade

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

# Input model for POST/PUT
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
    def post(self):
        """
        Create a new user
        """
        data = api.payload

        # --- VALIDATION ---
        required_fields = ["first_name", "last_name", "email", "password"]
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            api.abort(400, f"Missing required field(s): {', '.join(missing)}")

        # Create user
