from app import db, ma
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from argon2 import PasswordHasher


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        exclude = ["password_hash"]
        include_fk = True


auth_bp = Blueprint("auth", __name__, url_prefix=None)


@auth_bp.route("/register", methods=["POST"])
def register():
    user_schema = UserSchema()
    email = request.json["email"]
    if Users.query.filter_by(email=email).first():
        return jsonify({"message": "Email already in use"}), 409
    password = request.json["password"]
    hashed_password = PasswordHasher().hash(password)
    user = Users(email=email, password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))

