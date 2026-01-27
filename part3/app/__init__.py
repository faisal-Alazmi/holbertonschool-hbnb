from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.api.v1.views import api
    app.register_blueprint(api)

    return app
