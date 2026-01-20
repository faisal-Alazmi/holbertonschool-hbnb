#!/usr/bin/env python3
"""
Quick verification that password hashing works
"""
from app import create_app
from app.models.user import User

# Create app context
app = create_app()

with app.app_context():
    # Create a user
    user = User(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        password="plainTextPassword"
    )
    
    print("=== Password Hashing Verification ===")
    print(f"Original password: plainTextPassword")
    print(f"Hashed password: {user.password}")
    print(f"Password is hashed: {user.password != 'plainTextPassword'}")
    print(f"Hash starts with bcrypt prefix: {user.password.startswith('$2b$')}")
    print()
    
    print("=== Password Verification ===")
    print(f"Correct password verification: {user.verify_password('plainTextPassword')}")
    print(f"Incorrect password verification: {user.verify_password('wrongPassword')}")
    print()
    
    print("=== Serialization Check ===")
    user_dict = user.to_dict()
    print(f"Password in to_dict(): {'password' in user_dict}")
    print(f"Fields in to_dict(): {list(user_dict.keys())}")
