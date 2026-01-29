from flask import Flask
from flask_bcrypt import Bcrypt
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
