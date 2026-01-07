from app.models.base import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email):
        super().__init__()

        if not email:
            raise ValueError("Email is required")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email

        self.places = []   # places owned
        self.reviews = []  # reviews written
