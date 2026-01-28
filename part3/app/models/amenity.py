from app.models.base import BaseModel


class Amenity(BaseModel):
    def __init__(self, name: str):
        super().__init__()

        if not name:
            raise ValueError("Amenity name is required")

        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

