from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("places", description="Place operations")

place_input = api.model("PlaceInput", {
    "title": fields.String(required=True),
    "description": fields.String,
    "price": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "owner_id": fields.String(required=True),
    "amenities": fields.List(fields.String)
})


def serialize_place(place):
    owner = facade.get_user(place.owner_id)
    amenities = [
        facade.get_amenity(a_id).to_dict()
        for a_id in place.amenities
        if facade.get_amenity(a_id)
    ]

    return place.to_dict(
        owner=owner.to_dict() if owner else None,
        amenities=amenities
    )


@api.route("/")
class PlaceList(Resource):

    @api.expect(place_input)
    def post(self):
        try:
            place = facade.create_place(api.payload)
            return serialize_place(place), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    def get(self):
        places = facade.get_all_places()
        return [serialize_place(p) for p in places], 200


@api.route("/<string:place_id>")
class PlaceResource(Resource):

    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return serialize_place(place), 200

    def put(self, place_id):
        place = facade.update_place(place_id, api.payload)
        if not place:
            return {"error": "Place not found"}, 404
        return serialize_place(place), 200
