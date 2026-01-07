from app.models.base import BaseModel

class Place(BaseModel):
    def __init__(self, title, price, owner):
        super().__init__()

        if not title:
            raise ValueError("Title is required")
        if price < 0:
            raise ValueError("Price must be positive")

        self.title = title
        self.price = price
        self.owner = owner

        self.reviews = []
        self.amenities = []
