from marshmallow import EXCLUDE, fields
from marshmallow.exceptions import ValidationError
from app import SQLAlchemyAutoCamelCaseSchema, db, ma, jwt
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from argon2 import PasswordHasher
import sys
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )


class UserSchema(SQLAlchemyAutoCamelCaseSchema):
    class Meta:
        model = User
        exclude = ["password_hash"]
        include_fk = True


def validate_password(password: str):
    """
    Validates the password to ensure it meets the required criteria.
    """
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    if not password.isascii():
        raise ValidationError("Password must contain only ASCII characters")


class CreateUserSchema(ma.Schema):
    """
    Schema for creating a new user.
    """

    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate_password)

    class Meta:
        unknown = EXCLUDE


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user.
    """
    data = CreateUserSchema().load(request.get_json())
    email = data["email"]
    if User.query.filter(User.email.collate(email)).first():
        return jsonify({"message": "Email already in use"}), 409
    password = data["password"]
    hashed_password = PasswordHasher().hash(password)
    user = User(email=email, password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify(dict(message="User successfully created")), 201


# Returns the AUTH token if the user is user is authenticated
@auth_bp.route("/login", methods=["GET", "POST"])
@jwt_required(optional=True)
def login():
    """
    Authenticates a user and returns a JWT token in the response header.
    Sending a GET request returns the currently authenticated user's data.
    """
    if request.method == "GET":
        if user := get_jwt_identity():
            return jsonify(user), 200
        else:
            return jsonify({"message": "User not logged in"}), 401
    else:
        user_schema = UserSchema()
        email = request.json["email"]
        password = request.json["password"]
        if not (user := User.query.filter_by(email=email).first()):
            return jsonify({"message": "Invalid email or password"}), 401
        try:
            PasswordHasher().verify(user.password_hash, password)
        except:
            return jsonify({"message": "Invalid email or password "}), 401
        dump_user = user_schema.dump(user)
        token = create_access_token(identity=dump_user)
        return jsonify(dump_user), 200, {"Authorization": f"Bearer {token}"}


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
# @jwt.user_identity_loader
# def user_identity_lookup(user):
#     return user


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity["id"]).one_or_none()
