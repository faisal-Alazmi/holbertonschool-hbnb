from app import db
from app.models.base import BaseModel


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref='reviews', lazy=True)
    # Note: place relationship is defined in Place model with backref='place'

    def __init__(self, text, rating, user_id, place_id, **kwargs):
        if not text or not text.strip():
            raise ValueError("Review text is required and cannot be empty")
        if len(text) > 500:
            raise ValueError("Review text cannot exceed 500 characters")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        if not user_id:
            raise ValueError("User is required")
        if not place_id:
            raise ValueError("Place is required")

        super().__init__(
            text=text.strip(),
            rating=rating,
            user_id=user_id,
            place_id=place_id,
            **kwargs
        )

    def to_dict(self, user=None, place=None):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "user": user,
            "place": place,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

