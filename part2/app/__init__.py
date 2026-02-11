from flask import Flask
from app.api.v1 import init_api
from config import DevelopmentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    init_api(app)
    return app
