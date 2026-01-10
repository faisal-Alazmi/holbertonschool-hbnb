"""
Complete Unit Test Suite for HBnB API
Run with: pytest tests/ -v --cov=app
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.services import facade

@pytest.fixture
def app():
    """Create and configure test app"""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture(autouse=True)
def reset_facade():
    """Reset facade storage before each test"""
    facade.user_repo._storage.clear()
    facade.place_repo._storage.clear()
    facade.review_repo._storage.clear()
    facade.amenity_repo._storage.clear()
    yield

# ============================================================================
# USER TESTS
# ============================================================================

class TestUserModel:
    """Test User model validation"""
    
    def test_valid_user_creation(self):
        """Test creating a valid user"""
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@test.com',
            'password': 'pass123'
        }
        user = facade.create_user(user_data)
        assert user.first_name == 'John'
        assert user.last_name == 'Doe'
        assert user.email == 'john@test.com'
        assert user.id is not None
    
    def test_user_missing_first_name(self):
        """Test that missing first_name raises error"""
        with pytest.raises(ValueError, match="First name is required"):
            facade.create_user({
                'first_name': None,
                'last_name': 'Doe',
                'email': 'test@test.com',
                'password': 'pass'
            })
    
    def test_user_missing_email(self):
        """Test that missing email raises error"""
        with pytest.raises(ValueError, match="Email is required"):
            facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': None,
                'password': 'pass'
            })
    
    def test_user_missing_password(self):
        """Test that missing password raises error"""
        with pytest.raises(ValueError, match="Password is required"):
            facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'test@test.com',
                'password': None
            })

class TestUserEndpoints:
    """Test User API endpoints"""
    
    def test_create_user_success(self, client):
        """Test successful user creation via API"""
        response = client.post('/api/v1/users/', json={
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@test.com',
            'password': 'secure123'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['first_name'] == 'Jane'
        assert data['email'] == 'jane@test.com'
        assert 'id' in data
        assert 'password' not in data  # Password should not be in response
    
    def test_create_user_missing_fields(self, client):
        """Test creating user with missing fields"""
        response = client.post('/api/v1/users/', json={
            'first_name': 'John'
        })
        assert response.status_code == 400
        assert 'error' in response.get_json() or 'message' in response.get_json()
    
    def test_get_all_users(self, client):
        """Test getting all users"""
        # Create test user first
        client.post('/api/v1/users/', json={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@test.com',
            'password': 'pass'
        })
        
        response = client.get('/api/v1/users/')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_user_by_id(self, client):
        """Test getting specific user"""
        # Create user
        create_response = client.post('/api/v1/users/', json={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@test.com',
            'password': 'pass'
        })
        user_id = create_response.get_json()['id']
        
        # Get user
        response = client.get(f'/api/v1/users/{user_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == user_id

# ============================================================================
# PLACE TESTS
# ============================================================================

class TestPlaceModel:
    """Test Place model validation"""
    
    def test_valid_place_creation(self):
        """Test creating a valid place"""
        user = facade.create_user({
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@test.com',
            'password': 'pass'
        })
        
        place_data = {
            'title': 'Beach House',
            'description': 'Nice view',
            'price': 150.0,
            'latitude': 25.7617,
            'longitude': -80.1918,
            'owner_id': user.id,
            'amenities': []
        }
        place = facade.create_place(place_data)
        assert place.title == 'Beach House'
        assert place.price == 150.0
        assert place.owner_id == user.id
    
    def test_place_missing_title(self):
        """Test that missing title raises error"""
        user = facade.create_user({
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@test.com',
            'password': 'pass'
        })
        
        with pytest.raises(ValueError, match="Title is required"):
            facade.create_place({
                'title': None,
                'price': 100.0,
                'latitude': 40.0,
                'longitude': -74.0,
                'owner_id': user.id
            })
    
    def test_place_negative_price(self):
        """Test that negative price raises error"""
        user = facade.create_user({
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@test.com',
            'password': 'pass'
        })
        
        with pytest.raises(ValueError, match="Price must be positive"):
            facade.create_place({
                'title': 'Test',
                'price': -50.0,
                'latitude': 40.0,
                'longitude': -74.0,
                'owner_id': user.id
            })
    
    def test_place_invalid_latitude(self):
        """Test that invalid latitude raises error"""
        user = facade.create_user({
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@test.com',
            'password': 'pass'
        })
        
        with pytest.raises(ValueError, match="Invalid latitude"):
            facade.create_place({
                'title': 'Test',
                'price': 100.0,
                'latitude': 100.0,  # > 90
                'longitude': -74.0,
                'owner_id': user.id
            })
    
    def test_place_invalid_longitude(self):
        """Test that invalid longitude raises error"""
        user = facade.create_user({
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@test.com',
            'password': 'pass'
        })
        
        with pytest.raises(ValueError, match="Invalid longitude"):
            facade.create_place({
                'title': 'Test',
                'price': 100.0,
                'latitude': 40.0,
                'longitude': 200.0,  # > 180
                'owner_id': user.id
            })
    
    def test_place_invalid_owner(self):
        """Test that invalid owner_id raises error"""
        with pytest.raises(ValueError, match="Owner not found"):
            facade.create_place({
                'title': 'Test',
                'price': 100.0,
                'latitude': 40.0,
                'longitude': -74.0,
                'owner_id': 'fake-id'
            })

class TestPlaceEndpoints:
    """Test Place API endpoints"""
    
    def test_create_place_success(self, client):
        """Test successful place creation"""
        # Create owner first
        user_response = client.post('/api/v1/users/', json={
            'first_name': 'Owner',
            'last_name': 'Test',
            'email': 'owner@test.com',
            'password': 'pass'
        })
        owner_id = user_response.get_json()['id']
        
        # Create place
        response = client.post('/api/v1/places/', json={
            'title': 'Cozy Apartment',
            'description': 'Downtown location',
            'price': 120.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': owner_id,
            'amenities': []
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'Cozy Apartment'
        assert data['price'] == 120.0
    
    def test_create_place_invalid_owner(self, client):
        """Test creating place with invalid owner"""
        response = client.post('/api/v1/places/', json={
            'title': 'Test Place',
            'description': 'Test',
            'price': 100.0,
            'latitude': 40.0,
            'longitude': -74.0,
            'owner_id': 'invalid-id',
            'amenities': []
        })
        assert response.status_code == 400
    
    def test_get_all_places(self, client):
        """Test getting all places"""
        response = client.get('/api/v1/places/')
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)
    
    def test_get_place_by_id(self, client):
        """Test getting specific place"""
        # Create owner and place
        user_response = client.post('/api/v1/users/', json={
            'first_name': 'Owner',
            'last_name': 'Test',
            'email': 'owner@test.com',
            'password': 'pass'
        })
        owner_id = user_response.get_json()['id']
        
        place_response = client.post('/api/v1/places/', json={
            'title': 'Test Place',
            'description': 'Test',
            'price': 100.0,
            'latitude': 40.0,
            'longitude': -74.0,
            'owner_id': owner_id,
            'amenities': []
        })
        place_id = place_response.get_json()['id']
        
        # Get place
        response = client.get(f'/api/v1/places/{place_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == place_id

# ============================================================================
# REVIEW TESTS
# ============================================================================

class TestReviewModel:
    """Test Review model validation"""
    
    def test_valid_review_creation(self):
        """Test creating a valid review"""
        user = facade.create_user({
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@test.com',
            'password': 'pass'
        })
        
        place = facade.create_place({
            'title': 'Test Place',
            'price': 100.0,
            'latitude': 40.0,
            'longitude': -74.0,
            'owner_id': user.id
        })
        
        review = facade.create_review({
            'text': 'Great place!',
            'user_id': user.id,
            'place_id': place.id
        })
        assert review.text == 'Great place!'
        assert review.user_id == user.id
        assert review.place_id == place.id
    
    def test_review_missing_text(self):
        """Test that missing text raises error"""
        user = facade.create_user({
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@test.com',
            'password': 'pass'
        })
        
        place = facade.create_place({
            'title': 'Test Place',
            'price': 100.0,
            'latitude': 40.0,
            'longitude': -74.0,
            'owner_id': user.id
        })
        
        with pytest.raises(ValueError, match="Text is required"):
            facade.create_review({
                'text': None,
                'user_id': user.id,
                'place_id': place.id
            })
    
    def test_review_invalid_user(self):
        """Test that invalid user_id raises error"""
        user = facade.create_user({
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@test.com',
            'password': 'pass'
        })
        
        place = facade.create_place({
            'title': 'Test Place',
            'price': 100.0,
            'latitude': 40.0,
            'longitude': -74.0,
            'owner_id': user.id
        })
        
        with pytest.raises(ValueError, match="User not found"):
            facade.create_review({
                'text': 'Test',
                'user_id': 'fake-id',
                'place_id': place.id
            })
    
    def test_review_invalid_place(self):
        """Test that invalid place_id raises error"""
        user = facade.create_user({
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@test.com',
            'password': 'pass'
        })
        
        with pytest.raises(ValueError, match="Place not found"):
            facade.create_review({
                'text': 'Test',
                'user_id': user.id,
                'place_id': 'fake-id'
            })

class TestReviewEndpoints:
    """Test Review API endpoints"""
    
    def test_create_review_success(self, client):
        """Test successful review creation"""
        # Create user and place
        user_response = client.post('/api/v1/users/', json={
            'first_name': 'User',
            'last_name': 'Test',
            'email': 'user@test.com',
            'password': 'pass'
        })
        user_id = user_response.get_json()['id']
        
        place_response = client.post('/api/v1/places/', json={
            'title': 'Test Place',
            'description': 'Test',
            'price': 100.0,
            'latitude': 40.0,
            'longitude': -74.0,
            'owner_id': user_id,
            'amenities': []
        })
        place_id = place_response.get_json()['id']
        
        # Create review
        response = client.post('/api/v1/reviews/', json={
            'text': 'Excellent stay!',
            'user_id': user_id,
            'place_id': place_id
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['text'] == 'Excellent stay!'
    
    def test_create_review_missing_user_id(self, client):
        """Test creating review without user_id"""
        response = client.post('/api/v1/reviews/', json={
            'text': 'Test',
            'place_id': 'some-id'
        })
        assert response.status_code == 400
    
    def test_get_all_reviews(self, client):
        """Test getting all reviews"""
        response = client.get('/api/v1/reviews/')
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)

# ============================================================================
# AMENITY TESTS
# ============================================================================

class TestAmenityModel:
    """Test Amenity model validation"""
    
    def test_valid_amenity_creation(self):
        """Test creating a valid amenity"""
        amenity = facade.create_amenity({'name': 'WiFi'})
        assert amenity.name == 'WiFi'
        assert amenity.id is not None
    
    def test_amenity_missing_name(self):
        """Test that missing name raises error"""
        with pytest.raises(ValueError, match="Name is required"):
            facade.create_amenity({'name': None})

class TestAmenityEndpoints:
    """Test Amenity API endpoints"""
    
    def test_create_amenity_success(self, client):
        """Test successful amenity creation"""
        response = client.post('/api/v1/amenities/', json={
            'name': 'Swimming Pool'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == 'Swimming Pool'
    
    def test_create_amenity_missing_name(self, client):
        """Test creating amenity without name"""
        response = client.post('/api/v1/amenities/', json={})
        assert response.status_code == 400
    
    def test_get_all_amenities(self, client):
        """Test getting all amenities"""
        # Create amenity first
        client.post('/api/v1/amenities/', json={'name': 'WiFi'})
        
        response = client.get('/api/v1/amenities/')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_amenity_by_id(self, client):
        """Test getting specific amenity"""
        create_response = client.post('/api/v1/amenities/', json={
            'name': 'Parking'
        })
        amenity_id = create_response.get_json()['id']
        
        response = client.get(f'/api/v1/amenities/{amenity_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == amenity_id
        assert data['name'] == 'Parking'

# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Test complex workflows across multiple entities"""
    
    def test_complete_workflow(self, client):
        """Test creating user, place, amenity, and review"""
        # 1. Create user
        user_response = client.post('/api/v1/users/', json={
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@test.com',
            'password': 'secure'
        })
        assert user_response.status_code == 201
        user_id = user_response.get_json()['id']
        
        # 2. Create amenity
        amenity_response = client.post('/api/v1/amenities/', json={
            'name': 'WiFi'
        })
        assert amenity_response.status_code == 201
        amenity_id = amenity_response.get_json()['id']
        
        # 3. Create place with amenity
        place_response = client.post('/api/v1/places/', json={
            'title': 'Modern Loft',
            'description': 'City center',
            'price': 200.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': user_id,
            'amenities': [amenity_id]
        })
        assert place_response.status_code == 201
        place_id = place_response.get_json()['id']
        
        # 4. Create review
        review_response = client.post('/api/v1/reviews/', json={
            'text': 'Amazing loft!',
            'user_id': user_id,
            'place_id': place_id
        })
        assert review_response.status_code == 201
        
        # 5. Verify place includes owner and amenities
        place_get = client.get(f'/api/v1/places/{place_id}')
        place_data = place_get.get_json()
        assert place_data['owner'] is not None
        assert place_data['owner']['id'] == user_id
        assert len(place_data['amenities']) == 1
        assert place_data['amenities'][0]['id'] == amenity_id

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=app', '--cov-report=html'])
