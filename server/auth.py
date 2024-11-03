from app import db, ma
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from argon2 import PasswordHasher
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


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
    return jsonify(dict(message="User successfully created")), 201


@auth_bp.route("/login", methods=["GET", "POST"])
@jwt_required(optional=True)
def login():
    if request.method == "GET":
        if user := get_jwt_identity():
            return jsonify(user), 200
        else:
            return jsonify({"message": "User not logged in"}), 401
    else:
        user_schema = UserSchema()
        email = request.json["email"]
        password = request.json["password"]
        if not (user := Users.query.filter_by(email=email).first()):
            return jsonify({"message": "Invalid email or password"}), 401
        if not PasswordHasher().verify(user.password_hash, password):
            return jsonify({"message": "Invalid email or password "}), 401
        token = create_access_token(identity=user_schema.dump(user))
        return jsonify(user_schema.dump(user)), 200, {"Authorization": f"Bearer {token}"}
