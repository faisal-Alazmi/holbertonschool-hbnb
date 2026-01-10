from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        data = api.payload or {}
        try:
            place = facade.create_place(data)
            return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id,
            'amenities': place.amenities,
            'created_at': place.created_at.isoformat(),
            'updated_at': place.updated_at.isoformat(),
        }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places with expanded owner and amenities"""
        places = facade.get_all_places()
        result = []
        for p in places:
            owner = facade.get_user(p.owner_id)
            owner_data = None
            if owner:
                owner_data = {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email,
                }
            amenity_items = []
            for aid in (p.amenities or []):
                a = facade.get_amenity(aid)
                if a:
                    amenity_items.append({'id': a.id, 'name': a.name})
            result.append({
                'id': p.id,
                'title': p.title,
                'description': p.description,
                'price': p.price,
                'latitude': p.latitude,
                'longitude': p.longitude,
                'owner': owner_data,
                'amenities': amenity_items,
                'created_at': p.created_at.isoformat(),
                'updated_at': p.updated_at.isoformat(),
            })
        return result, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
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
            return {'error': str(e)}, 400
