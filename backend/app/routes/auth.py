# app/routes/auth.py

from flask import request, session, jsonify, Blueprint
from flask_login import login_user  
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from app.models import User
from app.schemas import LoginSchema, SignupSchema

auth_bp = Blueprint("auth", __name__)

login_schema = LoginSchema()
signup_schema = SignupSchema()


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    errors = signup_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    new_user = User(
        email=data["email"],
        name=data["name"]
    )
    new_user.set_password(data["password"])

    db.session.add(new_user)
    db.session.commit()

    # Optionally log in the user immediately
    login_user(new_user)
    session["user_id"] = new_user.id

    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    errors = login_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    user = User.query.filter_by(email=data["email"]).first()
    if user and user.check_password(data["password"]):
        login_user(user)  
        session["user_id"] = user.id
        return jsonify({
            "id": user.id,
            "email": user.email,
            "name": user.name
        })
    else:
        return jsonify({"error": "Invalid email or password"}), 401