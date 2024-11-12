from datetime import datetime, timezone
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError, fields
from app import CamelCaseSchema, db, app
import base64 
import hashlib
import filetype
import os


upload_bp = Blueprint("upload", __name__, url_prefix="/upload")

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    path = db.Column(db.String(120), nullable=False, unique=True)
    mime = db.Column(db.String(120), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

class ProductUpload(db.Model):
    upload_id = db.Column(db.Integer, db.ForeignKey("upload.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), primary_key=True)
    upload = db.relationship("Upload", backref="product_upload")
    product = db.relationship("Product", backref="product_upload")
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

# Schema for uploading files to later be used through the API
# Product images are uploaded through this endpoint
class UploadSchema(CamelCaseSchema):
    # Optional field for the file name
    name = fields.String()
    # The base64 encoded file data
    file_data = fields.String(required=True)

def validate_file_data(file_data: str) -> bytes:
    try:
        return base64.b64decode(file_data)
    except Exception:
        raise ValidationError("Invalid base64 data")


# Product images are uploaded through this endpoint
@upload_bp.route("/", methods=["POST"])
@jwt_required()
def upload():
    data = UploadSchema().load(request.get_json())
    file_data = validate_file_data(data["file_data"])
    hash = hashlib.sha256(file_data).hexdigest()
    mime = filetype.guess_mime(file_data)
    if not mime:
        mime = "application/octet-stream"
    ext = filetype.get_type(mime=mime)
    path = f"{hash}.{ext}" 
    file = open(os.path.join(app.config["UPLOAD_FOLDER"], path), "wb")
    file.write(file_data)

    upload = Upload(path=path, mime=mime)
    db.session.add(upload)
    db.session.commit()
    return {"message": "Upload successful!", "hash": hash}, 201
