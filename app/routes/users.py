from flask import Blueprint, jsonify
from app.models import User

user_bp = Blueprint("users", __name__)

@user_bp.route("/", methods=["GET"])
def get_users():
    users = User.query.all()

    return jsonify([u.username for u in users])