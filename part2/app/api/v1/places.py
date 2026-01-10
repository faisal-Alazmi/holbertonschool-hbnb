from flask_restx import Namespace, Resource, fields from app.services import facade from app.api.v1.reviews import serialize_review api = Namespace("places", description="Place operations") place_input = api.model("PlaceInput", { "title": fields.String(required=True), "description": fields.String, "price": fields.Float(required=True), "latitude": fields.Float(required=True), "longitude": fields.Float(required=True), "owner_id": fields.String(required=True), "amenities": fields.List(fields.String) }) def serialize_place(place): owner = facade.get_user(place.owner_id) amenities = [ facade.get_amenity(a_id).to_dict() for a_id in place.amenities if facade.get_amenity(a_id) ] reviews = [serialize_review(r) for r in facade.get_reviews_by_place(place.id)] return { **place.to_dict( owner=owner.to_dict() if owner else None, amenities=amenities ), "reviews": reviews } @api.route("/") class PlaceList(Resource): @api.expect(place_input) def post(self): data = api.payload # --- VALIDATION --- required_fields = ["title", "price", "latitude", "longitude", "owner_id"] missing = [f for f in required_fields if not data.get(f)] if missing: return {"error": f"Missing required field(s): {', '.join(missing)}"}, 400 # Check owner exists owner = facade.get_user(data["owner_id"]) if not owner: return {"error": "Owner not found"}, 400 # Create place place = facade.create_place(data) return serialize_place(place), 201 def get(self): places = facade.get_all_places() return [serialize_place(p) for p in places], 200 @api.route("/<string:place_id>") class PlaceResource(Resource): def get(self, place_id): place = facade.get_place(place_id) if not place: return {"error": "Place not found"}, 404 return serialize_place(place), 200 def put(self, place_id): data = api.payload if not data: return {"error": "No data provided"}, 400 allowed_fields = ["title", "description", "price", "latitude", "longitude", "owner_id", "amenities"] invalid_fields = [k for k in data if k not in allowed_fields] if invalid_fields: return {"error": f"Invalid fields: {', '.join(invalid_fields)}"}, 400 # If updating owner_id, check it exists if "owner_id" in data and not facade.get_user(data["owner_id"]): return {"error": "Owner not found"}, 400 place = facade.update_place(place_id, data) if not place: return {"error": "Place not found"}, 404 return serialize_place(place), 200        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        owner = facade.get_user(place.owner_id)
        owner_data = None
        if owner:
            owner_data = {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email,
            }
        amenity_items = []
        for aid in (place.amenities or []):
            a = facade.get_amenity(aid)
            if a:
                amenity_items.append({'id': a.id, 'name': a.name})
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': owner_data,
            'amenities': amenity_items,
            'created_at': place.created_at.isoformat(),
            'updated_at': place.updated_at.isoformat(),
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data = api.payload or {}
        try:
            place = facade.update_place(place_id, data)
            if not place:
                return {'error': 'Place not found'}, 404
            return { 'message': 'Place updated successfully' }, 200
        except ValueError as e:
            return {'error': str(e)}, 400        data = api.payload

        # --- VALIDATION ---
        required_fields = ["title", "price", "latitude", "longitude", "owner_id"]
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            return {"error": f"Missing required field(s): {', '.join(missing)}"}, 400

        # Check owner exists
        owner = facade.get_user(data["owner_id"])
        if not owner:
            return {"error": "Owner not found"}, 400

        # Create place
        place = facade.create_place(data)
        return serialize_place(place), 201

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
        data = api.payload
        if not data:
            return {"error": "No data provided"}, 400

        allowed_fields = ["title", "description", "price", "latitude", "longitude", "owner_id", "amenities"]
        invalid_fields = [k for k in data if k not in allowed_fields]
        if invalid_fields:
            return {"error": f"Invalid fields: {', '.join(invalid_fields)}"}, 400

        # If updating owner_id, check it exists
        if "owner_id" in data and not facade.get_user(data["owner_id"]):
            return {"error": "Owner not found"}, 400

        place = facade.update_place(place_id, data)
        if not place:
            return {"error": "Place not found"}, 404
        return serialize_place(place), 200
