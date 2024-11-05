from datetime import datetime, timezone
from flask import Blueprint, Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from dotenv import dotenv_values

dotenv = dotenv_values(".env")
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["JWT_SECRET_KEY"] = dotenv["JWT_SECRET_KEY"]

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

api = Blueprint('api', __name__, url_prefix='/api')
from auth import auth_bp
from products import products_bp
from orders import orders_bp
api.register_blueprint(auth_bp)

app.register_blueprint(api)
