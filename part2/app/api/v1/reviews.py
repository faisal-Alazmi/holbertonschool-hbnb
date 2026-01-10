from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("reviews", description="Review operations")

review_input = api.model("ReviewInput", {
    "text": fields.String(required=True),
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True)
})


def serialize_review(review):
    user = facade.get_user(review.user_id)
    return review.to_dict(
        user=user.to_dict() if user else None
    )


@api.route("/")
class ReviewList(Resource):

    @api.expect(review_input)
    def post(self):
        try:
            review = facade.create_review(api.payload)
            return serialize_review(review), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    def get(self):
        reviews = facade.get_all_reviews()
        return [serialize_review(r) for r in reviews], 200


@api.route("/<string:review_id>")
class ReviewResource(Resource):

    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return serialize_review(review), 200

    def put(self, review_id):
        review = facade.update_review(review_id, api.payload)
        if not review:
            return {"error": "Review not found"}, 404
        return serialize_review(review), 200

    def delete(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        facade.delete_review(review_id)
        return {}, 204
