from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from ..db import db
from ..models.user import User

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.post("/signup")
def signup():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    name = (data.get("name") or "").strip()
    password = data.get("password") or ""

    if not email or not name or not password:
        return jsonify({"message": "email, name, and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "email already in use"}), 409

    user = User(email=email, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    login_user(user)  # start session after signup
    return jsonify({"user": user.to_dict()}), 201

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "invalid credentials"}), 401

    login_user(user)
    return jsonify({"user": user.to_dict()}), 200

@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "logged out"}), 200

@auth_bp.get("/me")
def me():
    if not current_user.is_authenticated:
        return jsonify({"user": None}), 200
    return jsonify({"user": current_user.to_dict()}), 200