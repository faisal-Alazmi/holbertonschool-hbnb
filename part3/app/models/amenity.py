from app import db
from app.models.base import BaseModel


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name: str, **kwargs):
        if not name:
            raise ValueError("Amenity name is required")

        super().__init__(name=name, **kwargs)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

