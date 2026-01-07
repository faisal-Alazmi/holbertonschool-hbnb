from app.models.base import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password):
        super().__init__()

        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password  # ❌ لا نرجعه في API

        self.places = []
        self.reviews = []

    def to_dict(self):
        """
        Serialize user without password
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
