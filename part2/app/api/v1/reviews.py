from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.utils.auth import jwt_required

api = Namespace("reviews", description="Review operations")

# Input model for POST/PUT
review_input = api.model("ReviewInput", {
    "text": fields.String(required=True),
    "place_id": fields.String(required=True)
})

# Serializer
def serialize_review(review):
    user = facade.get_user(review.user_id)
    place = facade.get_place(review.place_id)
    return review.to_dict(
        user=user.to_dict() if user else None,
        place=place.to_dict() if place else None
    )

# --- Review List Endpoint ---
@api.route("/")
class ReviewList(Resource):
    @api.expect(review_input)
    @api.response(201, 'Review created successfully')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @jwt_required
    def post(self, current_user):
        """Create a new review (requires authentication)"""
        data = api.payload

        # --- VALIDATION ---
        required_fields = ["text", "place_id"]
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            return {"error": f"Missing required field(s): {', '.join(missing)}"}, 400

        # Use authenticated user's ID
        data["user_id"] = current_user.id

        # Check place exists
        if not facade.get_place(data["place_id"]):
            return {"error": "Place not found"}, 400

        # Create review with validations (owner check, duplicate check in facade)
        try:
            review = facade.create_review(data)
            return serialize_review(review), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return [serialize_review(r) for r in reviews], 200

# --- Review Resource Endpoint ---
@api.route("/<string:review_id>")
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get a specific review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return serialize_review(review), 200

    @api.expect(review_input)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden - not the owner')
    @api.response(404, 'Review not found')
    @jwt_required
    def put(self, current_user, review_id):
        """Update a review (requires authentication and ownership)"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        # Check ownership
        if review.user_id != current_user.id:
            return {"error": "You do not have permission to update this review"}, 403

        data = api.payload
        if not data:
            return {"error": "No data provided"}, 400

        # Only allow updating text
        allowed_fields = ["text"]
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not update_data:
            return {"error": "No valid fields to update"}, 400

        review = facade.update_review(review_id, update_data)
        if not review:
            return {"error": "Review not found"}, 404
        return serialize_review(review), 200

    @api.response(204, 'Review deleted successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden - not the owner')
    @api.response(404, 'Review not found')
    @jwt_required
    def delete(self, current_user, review_id):
        """Delete a review (requires authentication and ownership)"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        # Check ownership
        if review.user_id != current_user.id:
            return {"error": "You do not have permission to delete this review"}, 403

        facade.delete_review(review_id)
        return {}, 204
