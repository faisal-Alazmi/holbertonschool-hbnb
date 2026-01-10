from app.models.base import BaseModel


class Place(BaseModel):
    def __init__(
        self,
        title,
        price,
        latitude,
        longitude,
        owner_id,
        description=None,
        amenities=None
    ):
        super().__init__()

        if not title:
            raise ValueError("Title is required")
        if price <= 0:
            raise ValueError("Price must be positive")
        if not (-90 <= latitude <= 90):
            raise ValueError("Invalid latitude")
        if not (-180 <= longitude <= 180):
            raise ValueError("Invalid longitude")
        if not owner_id:
            raise ValueError("Owner is required")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = amenities or []

    def to_dict(self, owner=None, amenities=None):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": owner,
            "amenities": amenities or [],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
