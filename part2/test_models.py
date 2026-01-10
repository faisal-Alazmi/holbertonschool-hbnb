"""
Model Unit Tests - tests/test_models.py
Tests validation logic in models without API endpoints
Run with: pytest tests/test_models.py -v
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# ============================================================================
# USER MODEL TESTS
# ============================================================================

class TestUserModel:
    """Test User model validation"""
    
    def test_user_creation_valid(self):
        """Test creating a valid user"""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="secure123"
        )
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.id is not None
        print("✅ User creation test passed!")
    
    def test_user_missing_first_name(self):
        """Test that missing first_name raises ValueError"""
        with pytest.raises(ValueError, match="First name is required"):
            User(
                first_name=None,
                last_name="Doe",
                email="test@example.com",
                password="pass"
            )
    
    def test_user_missing_last_name(self):
        """Test that missing last_name raises ValueError"""
        with pytest.raises(ValueError, match="Last name is required"):
            User(
                first_name="John",
                last_name=None,
                email="test@example.com",
                password="pass"
            )
    
    def test_user_missing_email(self):
        """Test that missing email raises ValueError"""
        with pytest.raises(ValueError, match="Email is required"):
            User(
                first_name="John",
                last_name="Doe",
                email=None,
                password="pass"
            )
    
    def test_user_missing_password(self):
        """Test that missing password raises ValueError"""
        with pytest.raises(ValueError, match="Password is required"):
            User(
                first_name="John",
                last_name="Doe",
                email="test@example.com",
                password=None
            )
    
    def test_user_to_dict(self):
        """Test user serialization"""
        user = User(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            password="secure"
        )
        user_dict = user.to_dict()
        assert user_dict['first_name'] == "Jane"
        assert user_dict['last_name'] == "Smith"
        assert user_dict['email'] == "jane@example.com"
        assert 'password' not in user_dict  # Password should not be exposed
        assert 'id' in user_dict
        assert 'created_at' in user_dict
        assert 'updated_at' in user_dict

# ============================================================================
# PLACE MODEL TESTS
# ============================================================================

class TestPlaceModel:
    """Test Place model validation"""
    
    def test_place_creation_valid(self):
        """Test creating a valid place"""
        place = Place(
            title="Cozy Apartment",
            description="A nice place to stay",
            price=100.0,
            latitude=37.7749,
            longitude=-122.4194,
            owner_id="owner-123"
        )
        assert place.title == "Cozy Apartment"
        assert place.description == "A nice place to stay"
        assert place.price == 100.0
        assert place.latitude == 37.7749
        assert place.longitude == -122.4194
        assert place.owner_id == "owner-123"
        assert place.amenities == []
        print("✅ Place creation test passed!")
    
    def test_place_missing_title(self):
        """Test that missing title raises ValueError"""
        with pytest.raises(ValueError, match="Title is required"):
            Place(
                title=None,
                price=100.0,
                latitude=40.0,
                longitude=-74.0,
                owner_id="owner-123"
            )
    
    def test_place_negative_price(self):
        """Test that negative price raises ValueError"""
        with pytest.raises(ValueError, match="Price must be positive"):
            Place(
                title="Test Place",
                price=-50.0,
                latitude=40.0,
                longitude=-74.0,
                owner_id="owner-123"
            )
    
    def test_place_zero_price(self):
        """Test that zero price raises ValueError"""
        with pytest.raises(ValueError, match="Price must be positive"):
            Place(
                title="Test Place",
                price=0.0,
                latitude=40.0,
                longitude=-74.0,
                owner_id="owner-123"
            )
    
    def test_place_invalid_latitude_high(self):
        """Test that latitude > 90 raises ValueError"""
        with pytest.raises(ValueError, match="Invalid latitude"):
            Place(
                title="Test Place",
                price=100.0,
                latitude=100.0,
                longitude=-74.0,
                owner_id="owner-123"
            )
    
    def test_place_invalid_latitude_low(self):
        """Test that latitude < -90 raises ValueError"""
        with pytest.raises(ValueError, match="Invalid latitude"):
            Place(
                title="Test Place",
                price=100.0,
                latitude=-100.0,
                longitude=-74.0,
                owner_id="owner-123"
            )
    
    def test_place_invalid_longitude_high(self):
        """Test that longitude > 180 raises ValueError"""
        with pytest.raises(ValueError, match="Invalid longitude"):
            Place(
                title="Test Place",
                price=100.0,
                latitude=40.0,
                longitude=200.0,
                owner_id="owner-123"
            )
    
    def test_place_invalid_longitude_low(self):
        """Test that longitude < -180 raises ValueError"""
        with pytest.raises(ValueError, match="Invalid longitude"):
            Place(
                title="Test Place",
                price=100.0,
                latitude=40.0,
                longitude=-200.0,
                owner_id="owner-123"
            )
    
    def test_place_missing_owner_id(self):
        """Test that missing owner_id raises ValueError"""
        with pytest.raises(ValueError, match="Owner is required"):
            Place(
                title="Test Place",
                price=100.0,
                latitude=40.0,
                longitude=-74.0,
                owner_id=None
            )
    
    def test_place_with_amenities(self):
        """Test place creation with amenities"""
        place = Place(
            title="Modern Loft",
            price=200.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id="owner-456",
            amenities=["amenity-1", "amenity-2"]
        )
        assert len(place.amenities) == 2
        assert "amenity-1" in place.amenities
        assert "amenity-2" in place.amenities
    
    def test_place_boundary_coordinates(self):
        """Test place with boundary latitude/longitude values"""
        # Test max values
        place1 = Place(
            title="North Pole",
            price=100.0,
            latitude=90.0,
            longitude=180.0,
            owner_id="owner-789"
        )
        assert place1.latitude == 90.0
        assert place1.longitude == 180.0
        
        # Test min values
        place2 = Place(
            title="South Pole",
            price=100.0,
            latitude=-90.0,
            longitude=-180.0,
            owner_id="owner-789"
        )
        assert place2.latitude == -90.0
        assert place2.longitude == -180.0

# ============================================================================
# REVIEW MODEL TESTS
# ============================================================================

class TestReviewModel:
    """Test Review model validation"""
    
    def test_review_creation_valid(self):
        """Test creating a valid review"""
        review = Review(
            text="Great place!",
            user_id="user-123",
            place_id="place-456"
        )
        assert review.text == "Great place!"
        assert review.user_id == "user-123"
        assert review.place_id == "place-456"
        print("✅ Review creation test passed!")
    
    def test_review_missing_text(self):
        """Test that missing text raises ValueError"""
        with pytest.raises(ValueError, match="Review text is required"):
            Review(
                text=None,
                user_id="user-123",
                place_id="place-456"
            )
    
    def test_review_empty_text(self):
        """Test that empty text raises ValueError"""
        with pytest.raises(ValueError, match="Review text is required"):
            Review(
                text="",
                user_id="user-123",
                place_id="place-456"
            )
    
    def test_review_whitespace_text(self):
        """Test that whitespace-only text raises ValueError"""
        with pytest.raises(ValueError, match="Review text is required"):
            Review(
                text="   ",
                user_id="user-123",
                place_id="place-456"
            )
    
    def test_review_missing_user_id(self):
        """Test that missing user_id raises ValueError"""
        with pytest.raises(ValueError, match="User is required"):
            Review(
                text="Great!",
                user_id=None,
                place_id="place-456"
            )
    
    def test_review_missing_place_id(self):
        """Test that missing place_id raises ValueError"""
        with pytest.raises(ValueError, match="Place is required"):
            Review(
                text="Great!",
                user_id="user-123",
                place_id=None
            )
    
    def test_review_text_trimming(self):
        """Test that review text is trimmed"""
        review = Review(
            text="  Great place!  ",
            user_id="user-123",
            place_id="place-456"
        )
        assert review.text == "Great place!"
        assert review.text[0] != " "
        assert review.text[-1] != " "

# ============================================================================
# AMENITY MODEL TESTS
# ============================================================================

class TestAmenityModel:
    """Test Amenity model validation"""
    
    def test_amenity_creation_valid(self):
        """Test creating a valid amenity"""
        amenity = Amenity(name="Wi-Fi")
        assert amenity.name == "Wi-Fi"
        assert amenity.id is not None
        print("✅ Amenity creation test passed!")
    
    def test_amenity_missing_name(self):
        """Test that missing name raises ValueError"""
        with pytest.raises(ValueError, match="Name is required"):
            Amenity(name=None)
    
    def test_amenity_empty_name(self):
        """Test that empty name raises ValueError"""
        with pytest.raises(ValueError, match="Name is required"):
            Amenity(name="")
    
    def test_amenity_to_dict(self):
        """Test amenity serialization"""
        amenity = Amenity(name="Parking")
        amenity_dict = amenity.to_dict()
        assert amenity_dict['name'] == "Parking"
        assert 'id' in amenity_dict
        assert 'created_at' in amenity_dict
        assert 'updated_at' in amenity_dict

# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    # Run with pytest
    pytest.main([__file__, '-v'])
