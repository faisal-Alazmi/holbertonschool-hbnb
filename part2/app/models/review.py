from app.models.base import BaseModel


class Review(BaseModel):
    def __init__(self, text, user_id, place_id):
        super().__init__()

        if not text:
            raise ValueError("Review text is required")
        if not user_id:
            raise ValueError("User is required")
        if not place_id:
            raise ValueError("Place is required")

        self.text = text
        self.user_id = user_id
        self.place_id = place_id

    def to_dict(self, user=None):
        return {
            "id": self.id,
            "text": self.text,
            "user": user,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
