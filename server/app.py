from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )


@app.route("/api/register", methods=["POST"])
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
