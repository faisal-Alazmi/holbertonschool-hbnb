from app import db
from app.models.base import BaseModel


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), nullable=False)

    def __init__(
        self,
        title,
        price,
        latitude,
        longitude,
        owner_id,
        description=None,
        amenities=None,
        **kwargs
    ):
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

        super().__init__(
            title=title,
            description=description,
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner_id=owner_id,
            **kwargs
        )
        self.amenities = amenities or []

    def to_dict(self, owner=None, amenities=None):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "owner": owner,
            "amenities": amenities or [],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

