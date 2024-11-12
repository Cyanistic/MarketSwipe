from datetime import datetime, timedelta
from typing import Any, Optional
from flask import Blueprint, Flask, Request, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
from dotenv import dotenv_values
import json
from werkzeug.wrappers import Response

dotenv = dotenv_values(".env")
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["JWT_SECRET_KEY"] = dotenv["JWT_SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

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

api = Blueprint("api", __name__, url_prefix="/api")
from auth import auth_bp
from products import products_bp
from orders import orders_bp
from cart import cart_bp

api.register_blueprint(auth_bp)
api.register_blueprint(products_bp)
api.register_blueprint(orders_bp)
api.register_blueprint(cart_bp)

app.register_blueprint(api)
