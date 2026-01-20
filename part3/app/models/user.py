from app.models.base import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()
        
        # Validation
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
        self.places = []
        self.reviews = []
        
        if password:
            self.hash_password(password)
    
    def hash_password(self, password):
        """Hash the password before storing it"""
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """Verify the password against the hashed password"""
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)
    
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
