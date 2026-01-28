from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt

from app.services import facade

api = Namespace("amenities", description="Amenity operations")

amenity_input = api.model(
    "AmenityInput",
    {
        "name": fields.String(required=True),
    },
)

amenity_output = api.model(
    "Amenity",
    {
        "id": fields.String,
        "name": fields.String,
        "created_at": fields.String,
        "updated_at": fields.String,
    },
)


def _is_admin():
    claims = get_jwt()
    return bool(claims.get("is_admin", False))


@api.route("/")
class AmenityList(Resource):
    @api.expect(amenity_input)
    @jwt_required()
    def post(self):
        """Create a new amenity (admin only)."""
        if not _is_admin():
            return {"error": "Admin privileges required"}, 403

        data = api.payload or {}
        if not data.get("name"):
            return {"error": "Missing required field: name"}, 400

        try:
            amenity = facade.create_amenity(data)
        except ValueError as e:
            return {"error": str(e)}, 400
        return amenity.to_dict(), 201

    @api.marshal_list_with(amenity_output)
    def get(self):
        """List all amenities (public)."""
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200


@api.route("/<string:amenity_id>")
class AmenityResource(Resource):
    @api.marshal_with(amenity_output)
    def get(self, amenity_id):
        """Retrieve a single amenity (public)."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity (admin only)."""
        if not _is_admin():
            return {"error": "Admin privileges required"}, 403

        data = api.payload or {}
        if not data or "name" not in data:
            return {"error": "Missing required field: name"}, 400

        amenity = facade.update_amenity(amenity_id, data)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity (admin only)."""
        if not _is_admin():
            return {"error": "Admin privileges required"}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        facade.delete_amenity(amenity_id)
        return {}, 204

