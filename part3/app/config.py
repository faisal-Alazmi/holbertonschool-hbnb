import os

class Config:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key-change-in-production")
    # Secret key used by Flask-JWT-Extended for signing JWTs
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY", "jwt-secret-key-change-in-production"
    )
    DEBUG = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')  # Must be set in production

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
