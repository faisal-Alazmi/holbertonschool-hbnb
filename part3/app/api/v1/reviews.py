from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.services import facade

api = Namespace("reviews", description="Review operations")


def _is_admin():
    claims = get_jwt()
    return bool(claims.get("is_admin", False))


review_input = api.model(
    "ReviewInput",
    {
        "text": fields.String(required=True),
        "user_id": fields.String(required=True),
        "place_id": fields.String(required=True),
    },
)


def serialize_review(review):
    user = facade.get_user(review.user_id)
    place = facade.get_place(review.place_id)
    return review.to_dict(
        user=user.to_dict() if user else None,
        place=place.to_dict() if place else None,
    )


@api.route("/")
class ReviewList(Resource):
    @api.expect(review_input)
    @jwt_required()
    def post(self):
        """Create a new review.

        - Regular users: user_id must match the authenticated user.
        - Admins: can create reviews on behalf of any user.
        """
        data = api.payload or {}

        required_fields = ["text", "user_id", "place_id"]
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            return {
                "error": f"Missing required field(s): {', '.join(missing)}"
            }, 400

        current_user_id = get_jwt_identity()
        admin = _is_admin()

        if not admin and data.get("user_id") != current_user_id:
            return {"error": "Unauthorized action"}, 403

        # Check related entities
        if not facade.get_user(data["user_id"]):
            return {"error": "User not found"}, 400
        if not facade.get_place(data["place_id"]):
            return {"error": "Place not found"}, 400

        review = facade.create_review(data)
        return serialize_review(review), 201

    def get(self):
        """List all reviews (public)."""
        reviews = facade.get_all_reviews()
        return [serialize_review(r) for r in reviews], 200


@api.route("/<string:review_id>")
class ReviewResource(Resource):
    def get(self, review_id):
        """Retrieve a single review (public)."""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return serialize_review(review), 200

    @jwt_required()
    def put(self, review_id):
        """Update a review.

        - Owner can update own reviews.
        - Admin can update any review (bypass ownership).
        """
        data = api.payload or {}
        if not data:
            return {"error": "No data provided"}, 400

        allowed_fields = ["text", "user_id", "place_id"]
        invalid_fields = [k for k in data if k not in allowed_fields]
        if invalid_fields:
            return {
                "error": f"Invalid fields: {', '.join(invalid_fields)}"
            }, 400

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        current_user_id = get_jwt_identity()
        admin = _is_admin()

        if not admin and review.user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        # Validate potential changes
        if "user_id" in data and not facade.get_user(data["user_id"]):
            return {"error": "User not found"}, 400
        if "place_id" in data and not facade.get_place(data["place_id"]):
            return {"error": "Place not found"}, 400

        updated = facade.update_review(review_id, data)
        return serialize_review(updated), 200

    @jwt_required()
    def delete(self, review_id):
        """Delete a review (owner or admin)."""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        current_user_id = get_jwt_identity()
        admin = _is_admin()

        if not admin and review.user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)
        return {}, 204

