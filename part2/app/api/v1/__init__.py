from flask_restx import Api
from app.api.v1.users import api as users_ns


def init_api(app):
    api = Api(app, version="1.0", title="HBnB API", doc="/api/v1/")
    api.add_namespace(users_ns, path="/api/v1/users")
