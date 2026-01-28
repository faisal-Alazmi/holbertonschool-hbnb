from datetime import datetime
import uuid


class BaseModel:
    """Base model providing id and timestamp fields."""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update(self, data: dict):
        """Update existing attributes from a dict and refresh timestamp."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()

