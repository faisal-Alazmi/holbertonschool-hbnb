from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("amenities", description="Amenity operations")

# Input and output models
amenity_input = api.model("AmenityInput", {
    "name": fields.String(required=True)
})

amenity_output = api.model("Amenity", {
    "id": fields.String,
    "name": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String
})

# --- Amenity List ---
@api.route("/")
class AmenityList(Resource):
    @api.expect(amenity_input)
    def post(self):
        data = api.payload
        if not data.get("name"):
            return {"error": "Missing required field: name"}, 400

        amenity = facade.create_amenity(data)
        return amenity.to_dict(), 201

    def get(self):
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200

# --- Amenity Resource ---
@api.route("/<string:amenity_id>")
class AmenityResource(Resource):
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    def put(self, amenity_id):
        data = api.payload
        if not data or "name" not in data:
            return {"error": "Missing required field: name"}, 400

        amenity = facade.update_amenity(amenity_id, data)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    def delete(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        facade.delete_amenity(amenity_id)
        return {}, 204
