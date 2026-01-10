from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("amenities", description="Amenity operations")

amenity_input = api.model("AmenityInput", {
    "name": fields.String(required=True)
})

amenity_output = api.model("Amenity", {
    "id": fields.String,
    "name": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String
})


@api.route("/")
class AmenityList(Resource):

    @api.expect(amenity_input)
    def post(self):
        """Create a new amenity"""
        amenity = facade.create_amenity(api.payload)
        return amenity.to_dict(), 201

    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200


@api.route("/<string:amenity_id>")
class AmenityResource(Resource):

    def get(self, amenity_id):
        """Get one amenity"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    def put(self, amenity_id):
        """Update amenity"""
        amenity = facade.update_amenity(amenity_id, api.payload)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200
