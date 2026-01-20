from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text, user_id, place_id):
        super().__init__()
        # Validation
        if not text or not text.strip():
            raise ValueError("Review text is required and cannot be empty")
        if len(text) > 500:
            raise ValueError("Review text cannot exceed 500 characters")
        if not user_id:
            raise ValueError("User is required")
        if not place_id:
            raise ValueError("Place is required")
        
        self.text = text.strip()
        self.user_id = user_id
        self.place_id = place_id
    
    def to_dict(self, user=None, place=None):
        '''FIXED: Now accepts both user and place parameters'''
        return {
            "id": self.id,
            "text": self.text,
            "user": user,
            "place": place,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
