"""Reset database and seed admin user. Run from part3 folder: python reset_db.py"""
import os
import sys

# run from part3 directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.config import DevelopmentConfig
from app import db
from app.services import facade

app = create_app(DevelopmentConfig)
with app.app_context():
    db.drop_all()
    db.create_all()

with app.app_context():
    try:
        facade.create_user({
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "password": "admin123",
            "is_admin": True,
        })
        print("Admin user created: admin@example.com / admin123")
    except Exception as e:
        print("Error creating admin:", e)
    try:
        admin = facade.get_user_by_email("admin@example.com")
        if admin:
            amenity = facade.create_amenity({"name": "Wi-Fi"})
            facade.create_place({
                "title": "Cozy Apartment in NYC",
                "description": "Located in the heart of Manhattan.",
                "price": 80,
                "latitude": 40.7128,
                "longitude": -74.0060,
                "owner_id": admin.id,
                "amenities": [amenity.id],
            })
            facade.create_place({
                "title": "Beach House in Miami",
                "description": "Ocean views.",
                "price": 150,
                "latitude": 25.7617,
                "longitude": -80.1918,
                "owner_id": admin.id,
                "amenities": [amenity.id],
            })
            facade.create_place({
                "title": "Budget Room",
                "description": "Simple and affordable.",
                "price": 8,
                "latitude": 40.7,
                "longitude": -74.0,
                "owner_id": admin.id,
                "amenities": [amenity.id],
            })
            print("Places created.")
    except Exception as e:
        print("Error creating places:", e)

print("Done. Start the API with: python run.py")
