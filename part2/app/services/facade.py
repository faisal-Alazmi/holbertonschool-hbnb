from datetime import datetime
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """Facade coordinating business logic across repositories and models."""

    def __init__(self):
        """Initialize in-memory repositories for all entities."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User methods
    def create_user(self, user_data): 
        """Create a new user with validation and email normalization."""
        if 'email' in user_data and user_data['email']:
            user_data['email'] = user_data['email'].strip().lower()
       
        if self.get_user_by_email(user_data.get('email')):
            raise ValueError("Email already registered")

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by id or None if missing."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Find a user by email or return None if not found."""
        if not email:
            return None
        return self.user_repo.get_by_attribute('email', email.strip().lower())

    def list_users(self):
        """Return all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id: str, data: dict):
        """Update user fields with validation; return updated user or None."""
        user = self.user_repo.get(user_id)
        if not user:
            return None
            
        # first_name
        if 'first_name' in data and data['first_name'] is not None:
            first_name = str(data['first_name']).strip()
            if not first_name or len(first_name) > 50:
                raise ValueError("first_name must be at most 50 characters")
            user.first_name = first_name
            
        # last_name     
        if 'last_name' in data and data['last_name'] is not None:
            last_name = str(data['last_name']).strip()
            if not last_name or len(last_name) > 50:
                raise ValueError("last_name must be at most 50 characters")
            user.last_name = last_name
            
        # email
        if 'email' in data and data['email'] is not None:
            email = str(data['email']).strip().lower()
            if not email or len(email) > 255:
                raise ValueError("email must be at most 255 characters")
            user.email = email
            
        # is_admin
        if 'is_admin' in data and data['is_admin'] is not None:
            user.is_admin = bool(data['is_admin'])
            
        user.updated_at = datetime.utcnow()
        return user

    # Place methods
    def create_place(self, place_data):
        """Create a place after validating owner_id and amenities IDs."""
        # Validate owner exists (we still store owner_id on the model)
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError("owner_id is required")
        if not self.user_repo.get(owner_id):
            raise ValueError("Owner not found")

        # Normalize amenities key and validate each amenity id
        amenity_ids = place_data.get('amenities', [])
        valid_ids = []
        for aid in amenity_ids:
            if not self.amenity_repo.get(aid):
                raise ValueError(f"Amenity not found: {aid}")
            valid_ids.append(aid)

        # Build Place with IDs (owner_id and amenities as list of ids)
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner_id=owner_id,
            amenities=valid_ids,
        )
        self.place_repo.add(place)
        return place
    

    def get_place(self, place_id):
        """Retrieve a place by id or None."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Return all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id: str, data: dict):
        """Update place fields with validation; return updated place or None."""
        place = self.place_repo.get(place_id)
        if not place:
            return None
            
        # title if present
        if 'title' in data and data['title'] is not None:
            title = str(data['title']).strip()
            if not title or len(title) > 100:
                raise ValueError("title must be at most 100 characters")
            place.title = title
            
        # description if present
        if 'description' in data and data['description'] is not None:
            description = str(data['description']).strip()      
            if not description or len(description) > 1000:
                raise ValueError("description must be at most 1000 characters")
            place.description = description
            
        # price if present
        if 'price' in data and data['price'] is not None:
            price = float(data['price'])
            if price <= 0:
                raise ValueError("price must be positive")
            place.price = price

        # latitude if present
        if 'latitude' in data and data['latitude'] is not None:
            latitude = float(data['latitude'])
            if latitude < -90 or latitude > 90:
                raise ValueError("latitude must be between -90 and 90")
            place.latitude = latitude
                
        # longitude if present
        if 'longitude' in data and data['longitude'] is not None:
            longitude = float(data['longitude'])    
            if longitude < -180 or longitude > 180:
                raise ValueError("longitude must be between -180 and 180")
            place.longitude = longitude
            
        place.updated_at = datetime.utcnow()
        return place

    # Amenity methods
    def create_amenity(self, amenity_data):
        """Create a new amenity after validating name."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by id or None."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Return all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        """Update an amenity's fields with validation; return updated amenity or None."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        
        # name
        if 'name' in data and data['name'] is not None:
            name = str(data['name']).strip()
            if not name or len(name) > 50:
                raise ValueError("name must be at most 50 characters")
            amenity.name = name
            
        amenity.updated_at = datetime.utcnow()
        return amenity 

    # Review methods
    def create_review(self, review_data):
        """Create a review after validating user/place existence and rating/text."""
        # Validate foreign keys
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        if not self.user_repo.get(user_id):
            raise ValueError("User not found")
        if not self.place_repo.get(place_id):
            raise ValueError("Place not found")

        rating = int(review_data.get('rating', 0))
        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")

        text = str(review_data.get('text', '')).strip()
        if not text:
            raise ValueError("text cannot be empty")

        review = Review(
            text=text,
            rating=rating,
            user_id=user_id,
            place_id=place_id,
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by id or None."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Return all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Return all reviews that belong to the given place_id."""
        return [r for r in self.review_repo.get_all() if r.place_id == place_id]

    def update_review(self, review_id, data):
        """Update review fields with validation; return updated review or None."""
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if 'text' in data and data['text'] is not None:
            text = str(data['text']).strip()
            if not text or len(text) > 1000:
                raise ValueError("text must be at most 1000 characters")
            review.text = text

        if 'rating' in data and data['rating'] is not None:
            rating = int(data['rating'])
            if rating < 1 or rating > 5:
                raise ValueError("rating must be between 1 and 5")
            review.rating = rating

        review.updated_at = datetime.utcnow()
        return review

    def delete_review(self, review_id):
        """Delete a review by id; return deleted review or None if missing."""
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return review
