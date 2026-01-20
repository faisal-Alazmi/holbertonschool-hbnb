from flask import Flask
from app.extensions import bcrypt
from app.api.v1 import init_api

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Bcrypt
    bcrypt.init_app(app)
    
    init_api(app)
    return app
