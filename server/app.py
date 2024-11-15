from datetime import datetime, timedelta
import os
from typing import Any, Optional
from flask import Blueprint, Flask, Request, jsonify, request
from flask_marshmallow.schema import Schema
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest, HTTPException, UnsupportedMediaType
from dotenv import dotenv_values
import json
from werkzeug.wrappers import Response

dotenv = dotenv_values(".env")
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["JWT_SECRET_KEY"] = dotenv["JWT_SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)


def on_json_loading_failed(self, e: Optional[ValueError]) -> Any:
    if e:
        raise BadRequest(
            response=Response(
                json.dumps({"message": "Invalid JSON"}),
                status=400,
                content_type="application/json",
            )
        )
    else:
        raise UnsupportedMediaType(
            response=Response(
                json.dumps({"message": "Content type must be application/json"}),
                status=415,
                content_type="application/json",
            )
        )


Request.on_json_loading_failed = on_json_loading_failed


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(Schema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

class SQLAlchemyAutoCamelCaseSchema(ma.SQLAlchemyAutoSchema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "type": e.name,
            "message": e.description,
        }
    )
    response.content_type = "application/json"
    return response


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    """
    Return JSON instead of HTML for schema validation errors.
        In other words, when the client sends invalid JSON data.
    """
    return jsonify(e.messages), 400

if app.config["UPLOAD_FOLDER"]:
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

api = Blueprint("api", __name__, url_prefix="/api")
from auth import auth_bp
from products import products_bp
from orders import orders_bp
from cart import cart_bp
from upload import upload_bp

api.register_blueprint(auth_bp)
api.register_blueprint(products_bp)
api.register_blueprint(orders_bp)
api.register_blueprint(cart_bp)
api.register_blueprint(upload_bp)

app.register_blueprint(api)
