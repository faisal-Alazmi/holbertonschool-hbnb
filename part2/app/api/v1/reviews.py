from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("reviews", description="Review operations")

# Input model for POST/PUT
review_input = api.model("ReviewInput", {
    "text": fields.String(required=True),
    "user_id": fields.String(required=True),
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
    def post(self):
        data = api.payload

        # --- VALIDATION ---
        required_fields = ["text", "user_id", "place_id"]
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            return {"error": f"Missing required field(s): {', '.join(missing)}"}, 400

        # Check user exists
        if not facade.get_user(data["user_id"]):
            return {"error": "User not found"}, 400

        # Check place exists
        if not facade.get_place(data["place_id"]):
            return {"error": "Place not found"}, 400

        # Create review
        review = facade.create_review(data)
        return serialize_review(review), 201

    def get(self):
        reviews = facade.get_all_reviews()
        return [serialize_review(r) for r in reviews], 200

# --- Review Resource Endpoint ---
@api.route("/<string:review_id>")
class ReviewResource(Resource):
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return serialize_review(review), 200

    def put(self, review_id):
        data = api.payload
        if not data:
            return {"error": "No data provided"}, 400

        allowed_fields = ["text", "user_id", "place_id"]
        invalid_fields = [k for k in data if k not in allowed_fields]
        if invalid_fields:
            return {"error": f"Invalid fields: {', '.join(invalid_fields)}"}, 400

        # If user_id is updated, check exists
        if "user_id" in data and not facade.get_user(data["user_id"]):
            return {"error": "User not found"}, 400

        # If place_id is updated, check exists
        if "place_id" in data and not facade.get_place(data["place_id"]):
            return {"error": "Place not found"}, 400

        review = facade.update_review(review_id, data)
        if not review:
            return {"error": "Review not found"}, 404
        return serialize_review(review), 200

    def delete(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        facade.delete_review(review_id)
        return {}, 204
