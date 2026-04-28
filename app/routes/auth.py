from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# 🔐 Register
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    # 🔴 Only one admin allowed
    if data.get("role") == "admin":
        existing_admin = User.query.filter_by(role="admin").first()
        if existing_admin:
            return jsonify({"msg": "Admin already exists"}), 400

    user = User(
        username=data["username"],
        password=generate_password_hash(data["password"]),
        role=data.get("role", "user")
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "msg": "User created",
        "username": user.username,
        "role": user.role,
        "user_id": user.id   # ✅ यहाँ भी दिखा सकते हो
    })


# 🔐 Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(username=data["username"]).first()

    if user and check_password_hash(user.password, data["password"]):
        token = create_access_token(identity=str(user.id))
        
        return jsonify({
            "msg": "Login successful",
            "token": token,
            "user_id": user.id,   # ✅ रखा है
            "role": user.role
        })

    return jsonify({"msg": "Invalid credentials"}), 401