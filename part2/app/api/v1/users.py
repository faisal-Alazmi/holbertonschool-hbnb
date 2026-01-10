# app/api/v1/users.py
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace("users", description="User operations")

# Create facade instance
facade = HBnBFacade()

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
    def post(self):
        data = api.payload

        # Validation
        required_fields = ["first_name", "last_name", "email", "password"]
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            api.abort(400, f"Missing required field(s): {', '.join(missing)}")

        user = facade.create_user(data)
        return user.to_dict(), 201

    @api.marshal_list_with(user_model)
    def get(self):
        users = facade.get_all_users()
        return [u.to_dict() for u in users], 200


@api.route("/<string:user_id>")
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict()

    @api.expect(user_input)
    @api.marshal_with(user_model)
    def put(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")

        data = api.payload
        user = facade.update_user(user_id, data)
        return user.to_dict()
