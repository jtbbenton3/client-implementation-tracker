from flask import Blueprint
from .auth import auth_bp

api = Blueprint("api", __name__, url_prefix="/api")
api.register_blueprint(auth_bp, url_prefix="/auth")