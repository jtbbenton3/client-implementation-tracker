from flask import Blueprint, jsonify, session
from ..models import User
from ..db import db

user_bp = Blueprint("user", __name__, url_prefix="/api/user")

@user_bp.get("/me")
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"message": "Not authenticated"}), 401
    user = db.session.get(User, user_id)
    return jsonify(user.to_dict()), 200