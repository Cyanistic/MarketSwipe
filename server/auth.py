from app import db
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

auth_bp = Blueprint("auth", __name__, url_prefix=None)

@auth_bp.route("/register", methods=["POST"])
def register():
    email = request.json["email"]
    password = request.json["password"]
    try:
        user = Users(email=email, password_hash=password)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(f"Error {e}")
    return jsonify({"message": "User created"})
