#!/usr/bin/env python3
"""
Test suite for HBnB models
Tests all SQLAlchemy models and their relationships
"""

import unittest
from datetime import datetime
from app import create_app, db
from app.config import TestingConfig
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Tear down test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_base_model_id_generation(self):
        """Test that BaseModel generates UUID for id"""
        user = User(
            first_name="Test",
            last_name="User",
            email="test@test.com",
            password="password123"
        )
        self.assertIsNotNone(user.id)
        self.assertIsInstance(user.id, str)
        self.assertEqual(len(user.id), 36)  # UUID format

    def test_base_model_timestamps(self):
        """Test that BaseModel sets created_at and updated_at"""
        user = User(
            first_name="Test",
            last_name="User",
            email="test@test.com",
            password="password123"
        )
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)


class TestUserModel(unittest.TestCase):
    """Test cases for User model"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Tear down test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        """Test creating a user"""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123"
        )
        db.session.add(user)
        db.session.commit()

        self.assertIsNotNone(user.id)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertFalse(user.is_admin)

    def test_user_password_hashing(self):
        """Test that password is hashed"""
        user = User(
            first_name="Test",
            last_name="User",
            email="test@test.com",
            password="password123"
        )
        self.assertIsNotNone(user.password)
        self.assertNotEqual(user.password, "password123")
        self.assertTrue(user.password.startswith("$2b$"))

    def test_user_password_verification(self):
        """Test password verification"""
        user = User(
            first_name="Test",
            last_name="User",
            email="test@test.com",
            password="password123"
        )
        self.assertTrue(user.verify_password("password123"))
        self.assertFalse(user.verify_password("wrongpassword"))

    def test_user_email_unique(self):
        """Test that email must be unique"""
        user1 = User(
            first_name="User",
            last_name="One",
            email="same@email.com",
            password="password123"
        )
        db.session.add(user1)
        db.session.commit()

        user2 = User(
            first_name="User",
            last_name="Two",
            email="same@email.com",
            password="password456"
        )
        db.session.add(user2)

        with self.assertRaises(Exception):
            db.session.commit()

    def test_user_required_fields(self):
        """Test that required fields are enforced"""
        with self.assertRaises(ValueError):
            User(
                first_name="",
                last_name="Doe",
                email="test@test.com",
                password="password123"
            )

        with self.assertRaises(ValueError):
            User(
                first_name="John",
                last_name="",
                email="test@test.com",
                password="password123"
            )

        with self.assertRaises(ValueError):
            User(
                first_name="John",
                last_name="Doe",
                email="",
                password="password123"
            )

    def test_user_to_dict(self):
        """Test user serialization"""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password123",
            is_admin=True
        )
        user_dict = user.to_dict()

        self.assertIn("id", user_dict)
        self.assertIn("first_name", user_dict)
        self.assertIn("last_name", user_dict)
        self.assertIn("email", user_dict)
        self.assertIn("is_admin", user_dict)
        self.assertIn("created_at", user_dict)
        self.assertIn("updated_at", user_dict)
        self.assertNotIn("password", user_dict)  # Password should not be in dict


class TestPlaceModel(unittest.TestCase):
    """Test cases for Place model"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user
        self.user = User(
            first_name="Test",
            last_name="Owner",
            email="owner@test.com",
            password="password123"
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Tear down test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_place_creation(self):
        """Test creating a place"""
        place = Place(
            title="Cozy Apartment",
            description="A nice place to stay",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=self.user.id
        )
        db.session.add(place)
        db.session.commit()

        self.assertIsNotNone(place.id)
        self.assertEqual(place.title, "Cozy Apartment")
        self.assertEqual(place.price, 100.0)
        self.assertEqual(place.owner_id, self.user.id)

    def test_place_owner_relationship(self):
        """Test place-owner relationship"""
        place = Place(
            title="Test Place",
            description="Test",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=self.user.id
        )
        db.session.add(place)
        db.session.commit()

        # Test forward relationship
        self.assertEqual(place.owner.email, self.user.email)

        # Test backward relationship
        self.assertIn(place, self.user.places)

    def test_place_price_validation(self):
        """Test that price must be positive"""
        with self.assertRaises(ValueError):
            Place(
                title="Test Place",
                description="Test",
                price=0,
                latitude=40.7128,
                longitude=-74.0060,
                owner_id=self.user.id
            )

        with self.assertRaises(ValueError):
            Place(
                title="Test Place",
                description="Test",
                price=-10,
                latitude=40.7128,
                longitude=-74.0060,
                owner_id=self.user.id
            )

    def test_place_coordinates_validation(self):
        """Test latitude and longitude validation"""
        with self.assertRaises(ValueError):
            Place(
                title="Test Place",
                description="Test",
                price=100.0,
                latitude=91,  # Invalid
                longitude=-74.0060,
                owner_id=self.user.id
            )

        with self.assertRaises(ValueError):
            Place(
                title="Test Place",
                description="Test",
                price=100.0,
                latitude=40.7128,
                longitude=181,  # Invalid
                owner_id=self.user.id
            )


class TestReviewModel(unittest.TestCase):
    """Test cases for Review model"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test user and place
        self.user = User(
            first_name="Test",
            last_name="User",
            email="user@test.com",
            password="password123"
        )
        db.session.add(self.user)
        db.session.commit()

        self.place = Place(
            title="Test Place",
            description="Test",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=self.user.id
        )
        db.session.add(self.place)
        db.session.commit()

    def tearDown(self):
        """Tear down test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_review_creation(self):
        """Test creating a review"""
        review = Review(
            text="Great place!",
            rating=5,
            user_id=self.user.id,
            place_id=self.place.id
        )
        db.session.add(review)
        db.session.commit()

        self.assertIsNotNone(review.id)
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user_id, self.user.id)
        self.assertEqual(review.place_id, self.place.id)

    def test_review_rating_validation(self):
        """Test rating validation (1-5)"""
        with self.assertRaises(ValueError):
            Review(
                text="Test",
                rating=0,  # Invalid
                user_id=self.user.id,
                place_id=self.place.id
            )

        with self.assertRaises(ValueError):
            Review(
                text="Test",
                rating=6,  # Invalid
                user_id=self.user.id,
                place_id=self.place.id
            )

    def test_review_relationships(self):
        """Test review relationships"""
        review = Review(
            text="Great place!",
            rating=5,
            user_id=self.user.id,
            place_id=self.place.id
        )
        db.session.add(review)
        db.session.commit()

        # Test user relationship
        self.assertEqual(review.user.email, self.user.email)
        self.assertIn(review, self.user.reviews)

        # Test place relationship
        self.assertEqual(review.place.title, self.place.title)
        self.assertIn(review, self.place.reviews)


class TestAmenityModel(unittest.TestCase):
    """Test cases for Amenity model"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Tear down test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_amenity_creation(self):
        """Test creating an amenity"""
        amenity = Amenity(name="WiFi")
        db.session.add(amenity)
        db.session.commit()

        self.assertIsNotNone(amenity.id)
        self.assertEqual(amenity.name, "WiFi")

    def test_amenity_name_required(self):
        """Test that name is required"""
        with self.assertRaises(ValueError):
            Amenity(name="")

    def test_amenity_name_unique(self):
        """Test that amenity name must be unique"""
        amenity1 = Amenity(name="WiFi")
        db.session.add(amenity1)
        db.session.commit()

        amenity2 = Amenity(name="WiFi")
        db.session.add(amenity2)

        with self.assertRaises(Exception):
            db.session.commit()


class TestPlaceAmenityRelationship(unittest.TestCase):
    """Test cases for Place-Amenity many-to-many relationship"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test data
        self.user = User(
            first_name="Test",
            last_name="Owner",
            email="owner@test.com",
            password="password123"
        )
        db.session.add(self.user)
        db.session.commit()

        self.place = Place(
            title="Test Place",
            description="Test",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=self.user.id
        )
        db.session.add(self.place)
        db.session.commit()

        self.wifi = Amenity(name="WiFi")
        self.pool = Amenity(name="Swimming Pool")
        db.session.add(self.wifi)
        db.session.add(self.pool)
        db.session.commit()

    def tearDown(self):
        """Tear down test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_amenities_to_place(self):
        """Test adding amenities to a place"""
        self.place.amenities.append(self.wifi)
        self.place.amenities.append(self.pool)
        db.session.commit()

        self.assertEqual(len(self.place.amenities), 2)
        self.assertIn(self.wifi, self.place.amenities)
        self.assertIn(self.pool, self.place.amenities)

    def test_access_places_from_amenity(self):
        """Test accessing places from an amenity"""
        self.place.amenities.append(self.wifi)
        db.session.commit()

        self.assertIn(self.place, self.wifi.places)

    def test_remove_amenity_from_place(self):
        """Test removing an amenity from a place"""
        self.place.amenities.append(self.wifi)
        self.place.amenities.append(self.pool)
        db.session.commit()

        self.place.amenities.remove(self.wifi)
        db.session.commit()

        self.assertEqual(len(self.place.amenities), 1)
        self.assertNotIn(self.wifi, self.place.amenities)
        self.assertIn(self.pool, self.place.amenities)


class TestCascadeDeletes(unittest.TestCase):
    """Test cascade delete behavior"""

    def setUp(self):
        """Set up test environment"""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test data
        self.user = User(
            first_name="Test",
            last_name="Owner",
            email="owner@test.com",
            password="password123"
        )
        db.session.add(self.user)
        db.session.commit()

        self.place = Place(
            title="Test Place",
            description="Test",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=self.user.id
        )
        db.session.add(self.place)
        db.session.commit()

    def tearDown(self):
        """Tear down test environment"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_delete_place_cascades_to_reviews(self):
        """Test that deleting a place deletes its reviews"""
        review = Review(
            text="Great place!",
            rating=5,
            user_id=self.user.id,
            place_id=self.place.id
        )
        db.session.add(review)
        db.session.commit()

        review_id = review.id

        # Delete the place
        db.session.delete(self.place)
        db.session.commit()

        # Review should be deleted
        deleted_review = db.session.get(Review, review_id)
        self.assertIsNone(deleted_review)


if __name__ == '__main__':
    unittest.main()
