#!/usr/bin/env python3
"""
Script to generate bcrypt password hash for admin user
Usage: python3 generate_password_hash.py
"""

try:
    import bcrypt

    password = "admin1234"
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print(f"Password: {password}")
    print(f"Bcrypt Hash: {hashed.decode('utf-8')}")
except ImportError:
    print("Error: bcrypt module not installed")
    print("Install it with: pip install bcrypt")
    print("\nFor now, using a pre-generated hash:")
    print("$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqGj1Gj9Da")
