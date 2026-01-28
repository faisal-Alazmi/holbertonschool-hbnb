from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from app.api.v1.init import init_api
from app.api.v1.views import api as health_blueprint

jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Extensions
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.route("/")
    def index():
        return {"message": "API at /api/v1/", "docs": "/api/v1/"}, 200

    # REST API (users, amenities, places, reviews, auth)
    init_api(app)

    # Simple health-check endpoint
    app.register_blueprint(health_blueprint)

    # Seed default admin user for testing (if no users exist)
    _seed_admin_if_needed()

    return app


def _seed_admin_if_needed():
    """Create a default admin user so admin endpoints can be tested."""
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
