from datetime import datetime
from app import db, bcrypt
from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    password = db.Column(db.String(256), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships (defined via backrefs from other models)
    # - places: one-to-many relationship with Place (backref from Place.owner)
    # - reviews: one-to-many relationship with Review (backref from Review.user)

    def __init__(self, first_name=None, last_name=None, email=None, password=None, is_admin=False, **kwargs):
        if not first_name:
            raise ValueError("First name is required")
        if not last_name:
            raise ValueError("Last name is required")
        if not email:
            raise ValueError("Email is required")

        super().__init__(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_admin=is_admin,
            **kwargs,
        )
        self.password = None
        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """Hash the password before storing it."""
        if not password:
            raise ValueError("Password is required")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
