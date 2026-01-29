from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.services import facade

api = Namespace("users", description="User operations")

user_model = api.model(
    "User",
    {
        "id": fields.String(readonly=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.String(required=True),
        "is_admin": fields.Boolean,
        "created_at": fields.String,
        "updated_at": fields.String,
    },
)

user_input = api.model(
    "UserInput",
    {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
        "is_admin": fields.Boolean(default=False),
    },
)


def _is_admin():
    claims = get_jwt()
    return bool(claims.get("is_admin", False))


@api.route("/")
class UserList(Resource):
    @api.expect(user_input)
    @api.marshal_with(user_model, code=201)
    @jwt_required()
    def post(self):
        if not _is_admin():
            return {"error": "Admin privileges required"}, 403

        data = api.payload or {}
        required_fields = ["first_name", "last_name", "email", "password"]
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            return {
                "error": f"Missing required field(s): {', '.join(missing)}"
            }, 400

        if facade.get_user_by_email(data.get("email")):
            return {"error": "Email already exists"}, 400

        try:
            user = facade.create_user(data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return user.to_dict(), 201

    @api.marshal_list_with(user_model)
    @jwt_required()
    def get(self):
        if not _is_admin():
            return {"error": "Admin privileges required"}, 403
        users = facade.get_all_users()
        return [u.to_dict() for u in users], 200


@api.route("/<string:user_id>")
class UserResource(Resource):
    @api.marshal_with(user_model)
    @jwt_required()
    def get(self, user_id):
        current_user_id = get_jwt_identity()
        if not _is_admin() and current_user_id != user_id:
            return {"error": "Forbidden"}, 403

        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user.to_dict()

    @api.expect(user_input)
    @api.marshal_with(user_model)
    @jwt_required()
    def put(self, user_id):
        if not _is_admin():
            return {"error": "Admin privileges required"}, 403

        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")

        data = api.payload or {}

        if "email" in data and data.get("email"):
            existing = facade.get_user_by_email(data["email"])
            if existing and existing.id != user_id:
                return {"error": "Email already in use"}, 400

        try:
            updated = facade.update_user(user_id, data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return updated.to_dict()

