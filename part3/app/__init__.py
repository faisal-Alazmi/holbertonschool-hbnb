from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

from app.api.v1.init import init_api
from app.api.v1.views import api as health_blueprint


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8000", "http://localhost:8000"])

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        return {"message": "API at /api/v1/", "docs": "/api/v1/"}, 200

    init_api(app)
    app.register_blueprint(health_blueprint)

    with app.app_context():
        _seed_admin_if_needed()
        _seed_places_if_needed()

    return app


def _seed_admin_if_needed():
    from app.services import facade

    if facade.get_all_users():
        return
    try:
        facade.create_user(
            {
                "first_name": "Admin",
                "last_name": "User",
                "email": "admin@example.com",
                "password": "admin123",
                "is_admin": True,
            }
        )
    except Exception:
        pass


def _seed_places_if_needed():
    from app.services import facade

    if facade.get_all_places():
        return
    try:
        admin = facade.get_user_by_email("admin@example.com")
        if not admin:
            return
        amenity = facade.create_amenity({"name": "Wi-Fi"})
        facade.create_place(
            {
                "title": "Cozy Apartment in NYC",
                "description": "Located in the heart of Manhattan, close to everything.",
                "price": 80,
                "latitude": 40.7128,
                "longitude": -74.0060,
                "owner_id": admin.id,
                "amenities": [amenity.id],
            }
        )
        facade.create_place(
            {
                "title": "Beach House in Miami",
                "description": "Enjoy the sun and ocean views from your balcony.",
                "price": 150,
                "latitude": 25.7617,
                "longitude": -80.1918,
                "owner_id": admin.id,
                "amenities": [amenity.id],
            }
        )
        facade.create_place(
            {
                "title": "Budget Room",
                "description": "Simple and affordable.",
                "price": 8,
                "latitude": 40.7,
                "longitude": -74.0,
                "owner_id": admin.id,
                "amenities": [amenity.id],
            }
        )
    except Exception:
        pass
