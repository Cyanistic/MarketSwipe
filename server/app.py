from datetime import datetime, timezone
from flask import Blueprint, Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

api = Blueprint('api', __name__, url_prefix='/api')
from auth import auth_bp
api.register_blueprint(auth_bp)

app.register_blueprint(api)
