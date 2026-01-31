#!/usr/bin/env python3
"""
Test suite for HBnB API endpoints
Tests all API endpoints with authentication and authorization
"""

import unittest
import json
from app import create_app, db
from app.config import TestingConfig
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class TestAuthEndpoints(unittest.TestCase):
    """Test authentication endpoints"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user
        self.user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="password123"
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Tear down test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_success(self):
        """Test successful login"""
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'test@example.com',
                'password': 'wrongpassword'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)

    def test_login_missing_fields(self):
        """Test login with missing fields"""
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'test@example.com'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


class TestUserEndpoints(unittest.TestCase):
    """Test user endpoints"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create admin user
        self.admin = User(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password="admin123",
            is_admin=True
        )
        db.session.add(self.admin)
        db.session.commit()

        # Get admin token
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'admin@example.com',
                'password': 'admin123'
            }),
            content_type='application/json'
        )
        self.admin_token = json.loads(response.data)['access_token']

    def tearDown(self):
        """Tear down test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user_as_admin(self):
        """Test creating a user as admin"""
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            }),
            headers={'Authorization': f'Bearer {self.admin_token}'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['email'], 'john@example.com')

    def test_create_user_without_auth(self):
        """Test that creating user without auth fails"""
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)

    def test_list_users_as_admin(self):
        """Test listing users as admin"""
        response = self.client.get(
            '/api/v1/users/',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_user_by_id(self):
        """Test getting user by ID"""
        response = self.client.get(
            f'/api/v1/users/{self.admin.id}',
            headers={'Authorization': f'Bearer {self.admin_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['email'], 'admin@example.com')

    def test_update_user(self):
        """Test updating user"""
        response = self.client.put(
            f'/api/v1/users/{self.admin.id}',
            data=json.dumps({
                'first_name': 'Updated'
            }),
            headers={'Authorization': f'Bearer {self.admin_token}'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Updated')


class TestAmenityEndpoints(unittest.TestCase):
    """Test amenity endpoints"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create admin user
        self.admin = User(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password="admin123",
            is_admin=True
        )
        db.session.add(self.admin)
        db.session.commit()

        # Get admin token
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'admin@example.com',
                'password': 'admin123'
            }),
            content_type='application/json'
        )
        self.admin_token = json.loads(response.data)['access_token']

    def tearDown(self):
        """Tear down test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_amenity_as_admin(self):
        """Test creating amenity as admin"""
        response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps({'name': 'WiFi'}),
            headers={'Authorization': f'Bearer {self.admin_token}'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'WiFi')

    def test_create_amenity_without_auth(self):
        """Test that creating amenity without admin fails"""
        response = self.client.post(
            '/api/v1/amenities/',
            data=json.dumps({'name': 'WiFi'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)

    def test_list_amenities_public(self):
        """Test that listing amenities is public"""
        # Create an amenity
        amenity = Amenity(name='WiFi')
        db.session.add(amenity)
        db.session.commit()

        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_get_amenity_by_id_public(self):
        """Test getting amenity by ID is public"""
        amenity = Amenity(name='WiFi')
        db.session.add(amenity)
        db.session.commit()

        response = self.client.get(f'/api/v1/amenities/{amenity.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'WiFi')

    def test_update_amenity_as_admin(self):
        """Test updating amenity as admin"""
        amenity = Amenity(name='WiFi')
        db.session.add(amenity)
        db.session.commit()

        response = self.client.put(
            f'/api/v1/amenities/{amenity.id}',
            data=json.dumps({'name': 'High-Speed WiFi'}),
            headers={'Authorization': f'Bearer {self.admin_token}'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'High-Speed WiFi')


class TestPlaceEndpoints(unittest.TestCase):
    """Test place endpoints"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test users
        self.user = User(
            first_name="Test",
            last_name="User",
            email="user@example.com",
            password="password123"
        )
        self.admin = User(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password="admin123",
            is_admin=True
        )
        db.session.add(self.user)
        db.session.add(self.admin)
        db.session.commit()

        # Get tokens
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'user@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        self.user_token = json.loads(response.data)['access_token']

        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'admin@example.com',
                'password': 'admin123'
            }),
            content_type='application/json'
        )
        self.admin_token = json.loads(response.data)['access_token']

    def tearDown(self):
        """Tear down test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_place_authenticated(self):
        """Test creating a place as authenticated user"""
        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps({
                'title': 'Cozy Apartment',
                'description': 'A nice place',
                'price': 100.0,
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': self.user.id
            }),
            headers={'Authorization': f'Bearer {self.user_token}'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Cozy Apartment')

    def test_create_place_without_auth(self):
        """Test that creating place without auth fails"""
        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps({
                'title': 'Cozy Apartment',
                'description': 'A nice place',
                'price': 100.0,
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': self.user.id
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)

    def test_list_places_public(self):
        """Test that listing places is public"""
        place = Place(
            title='Test Place',
            description='Test',
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=self.user.id
        )
        db.session.add(place)
        db.session.commit()

        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_update_place_as_owner(self):
        """Test updating place as owner"""
        place = Place(
            title='Test Place',
            description='Test',
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=self.user.id
        )
        db.session.add(place)
        db.session.commit()

        response = self.client.put(
            f'/api/v1/places/{place.id}',
            data=json.dumps({'title': 'Updated Place'}),
            headers={'Authorization': f'Bearer {self.user_token}'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Updated Place')

    def test_update_place_as_non_owner(self):
        """Test that non-owner cannot update place"""
        # Create another user
        other_user = User(
            first_name="Other",
            last_name="User",
            email="other@example.com",
            password="password123"
        )
        db.session.add(other_user)
        db.session.commit()

        # Get other user token
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'other@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        other_token = json.loads(response.data)['access_token']

        # Create place owned by first user
        place = Place(
            title='Test Place',
            description='Test',
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=self.user.id
        )
        db.session.add(place)
        db.session.commit()

        # Try to update as other user
        response = self.client.put(
            f'/api/v1/places/{place.id}',
            data=json.dumps({'title': 'Hacked'}),
            headers={'Authorization': f'Bearer {other_token}'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)


class TestReviewEndpoints(unittest.TestCase):
    """Test review endpoints"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test users
        self.user = User(
            first_name="Test",
            last_name="User",
            email="user@example.com",
            password="password123"
        )
        self.owner = User(
            first_name="Owner",
            last_name="User",
            email="owner@example.com",
            password="password123"
        )
        db.session.add(self.user)
        db.session.add(self.owner)
        db.session.commit()

        # Create a place
        self.place = Place(
            title='Test Place',
            description='Test',
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=self.owner.id
        )
        db.session.add(self.place)
        db.session.commit()

        # Get user token
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'user@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        self.user_token = json.loads(response.data)['access_token']

    def tearDown(self):
        """Tear down test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_review_authenticated(self):
        """Test creating a review as authenticated user"""
        response = self.client.post(
            '/api/v1/reviews/',
            data=json.dumps({
                'text': 'Great place!',
                'rating': 5,
                'user_id': self.user.id,
                'place_id': self.place.id
            }),
            headers={'Authorization': f'Bearer {self.user_token}'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['text'], 'Great place!')
        self.assertEqual(data['rating'], 5)

    def test_create_review_without_auth(self):
        """Test that creating review without auth fails"""
        response = self.client.post(
            '/api/v1/reviews/',
            data=json.dumps({
                'text': 'Great place!',
                'rating': 5,
                'user_id': self.user.id,
                'place_id': self.place.id
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)

    def test_list_reviews_public(self):
        """Test that listing reviews is public"""
        review = Review(
            text='Great place!',
            rating=5,
            user_id=self.user.id,
            place_id=self.place.id
        )
        db.session.add(review)
        db.session.commit()

        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_update_review_as_author(self):
        """Test updating review as author"""
        review = Review(
            text='Great place!',
            rating=5,
            user_id=self.user.id,
            place_id=self.place.id
        )
        db.session.add(review)
        db.session.commit()

        response = self.client.put(
            f'/api/v1/reviews/{review.id}',
            data=json.dumps({'text': 'Updated review', 'rating': 4}),
            headers={'Authorization': f'Bearer {self.user_token}'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['text'], 'Updated review')


class TestHealthEndpoint(unittest.TestCase):
    """Test health check endpoint"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Tear down test environment"""
        self.app_context.pop()

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/v1/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')


if __name__ == '__main__':
    unittest.main()
