from app.models.base import BaseModel
from app.extensions import bcrypt

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password):
        super().__init__()
        
        # Add these validation checks
        if not first_name:
            raise ValueError("First name is required")
        if not last_name:
            raise ValueError("Last name is required")
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)
        self.places = []
        self.reviews = []
    
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
    
    def update(self, data: dict):
        """Update user attributes, handling password hashing specially."""
        for key, value in data.items():
            if key == 'password':
                # Hash the password if it's being updated
                self.hash_password(value)
            elif hasattr(self, key):
                setattr(self, key, value)
        from datetime import datetime
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Serialize user without password"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
