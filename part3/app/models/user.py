from app.models.base import BaseModel
from app import bcrypt


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        """User model with hashed password and admin flag."""
        super().__init__()

        if not first_name:
            raise ValueError("First name is required")
        if not last_name:
            raise ValueError("Last name is required")
        if not email:
            raise ValueError("Email is required")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = None
        self.is_admin = is_admin

        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """Hash the password before storing."""
        if not password:
            raise ValueError("Password is required")
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Verify the password."""
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Convert to dictionary (exclude password)."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
