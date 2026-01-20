"""
Password Hashing Tests - tests/test_password_hashing.py
Tests password hashing functionality in User model
Run with: pytest test_password_hashing.py -v
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import bcrypt
from app.models.user import User

@pytest.fixture
def app():
    """Create and configure a test Flask app"""
    app = create_app()
    app.config['TESTING'] = True
    return app

class TestPasswordHashing:
    """Test password hashing functionality"""
    
    def test_password_is_hashed(self, app):
        """Test that password is hashed when user is created"""
        with app.app_context():
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password="plaintext123"
            )
            # Password should be hashed (not equal to plaintext)
            assert user.password != "plaintext123"
            # Hashed password should be a string
            assert isinstance(user.password, str)
            # Hashed password should start with bcrypt prefix
            assert user.password.startswith('$2b$')
    
    def test_verify_password_correct(self, app):
        """Test that verify_password returns True for correct password"""
        with app.app_context():
            user = User(
                first_name="Jane",
                last_name="Smith",
                email="jane@example.com",
                password="secret456"
            )
            # Correct password should verify
            assert user.verify_password("secret456") == True
    
    def test_verify_password_incorrect(self, app):
        """Test that verify_password returns False for incorrect password"""
        with app.app_context():
            user = User(
                first_name="Bob",
                last_name="Johnson",
                email="bob@example.com",
                password="mypassword"
            )
            # Incorrect password should not verify
            assert user.verify_password("wrongpassword") == False
    
    def test_password_not_in_to_dict(self, app):
        """Test that password is not included in to_dict() output"""
        with app.app_context():
            user = User(
                first_name="Alice",
                last_name="Williams",
                email="alice@example.com",
                password="supersecret"
            )
            user_dict = user.to_dict()
            # Password should not be in serialized output
            assert 'password' not in user_dict
            # Other fields should be present
            assert 'id' in user_dict
            assert 'first_name' in user_dict
            assert 'last_name' in user_dict
            assert 'email' in user_dict
    
    def test_different_users_different_hashes(self, app):
        """Test that same password produces different hashes for different users"""
        with app.app_context():
            user1 = User(
                first_name="User",
                last_name="One",
                email="user1@example.com",
                password="samepassword"
            )
            user2 = User(
                first_name="User",
                last_name="Two",
                email="user2@example.com",
                password="samepassword"
            )
            # Same password should produce different hashes (due to salt)
            assert user1.password != user2.password
            # But both should verify the same password
            assert user1.verify_password("samepassword") == True
            assert user2.verify_password("samepassword") == True
    
    def test_password_update_is_hashed(self, app):
        """Test that password is hashed when updated via update() method"""
        with app.app_context():
            user = User(
                first_name="Update",
                last_name="Test",
                email="update@example.com",
                password="oldpassword"
            )
            old_hash = user.password
            
            # Update password via update method
            user.update({"password": "newpassword"})
            
            # Password should be hashed (not equal to plaintext)
            assert user.password != "newpassword"
            # Password should have changed
            assert user.password != old_hash
            # New password should verify correctly
            assert user.verify_password("newpassword") == True
            # Old password should not verify
            assert user.verify_password("oldpassword") == False

if __name__ == "__main__":
    # Run with pytest
    pytest.main([__file__, '-v'])
