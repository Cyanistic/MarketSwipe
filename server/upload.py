from datetime import datetime, timezone
from typing import Optional
from flask import Blueprint, request, send_from_directory
from flask_jwt_extended import jwt_required
from marshmallow import EXCLUDE, ValidationError, fields
import sqlalchemy
from app import CamelCaseSchema, SQLAlchemyAutoCamelCaseSchema, db, app
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
class UploadRequestSchema(CamelCaseSchema):
    # Optional field for the file name
    name = fields.String()
    # The base64 encoded file data
    file_data = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE


class UploadSchema(SQLAlchemyAutoCamelCaseSchema):
    class Meta:
        model = Upload
        load_instance = True
        unknow = EXCLUDE


# Validates the base64 encoded file data and returns the decoded bytes
# data should be in the form of: "data:MIME_TYPE;base64,DATA"
def validate_file_data(file_data: str) -> tuple[bytes, Optional[str]]:
    try:
        # Remove the data type and encoding information from the data
        head, *raw_data = file_data.split(",")
        # If the raw data is empty, then the data has no encoding information
        if not raw_data:
                return base64.b64decode(file_data), None
        # If the raw data is not empty, then the data has encoding information
        # Split the encoding information from the MIME type
        # head = "data:MIME_TYPE"
        # tail = "base64"
        head, tail = head.split(";");
        if not tail or not head:
            raise ValidationError("Invalid base64 data")

        mime = head.split(":")[1]
        return base64.b64decode(raw_data[0]), mime
    except Exception:
        raise ValidationError("Invalid base64 data")




# Product images are uploaded through this endpoint
# Expects an UploadRequestSchema payload
@upload_bp.route("/", methods=["POST"])
@jwt_required()
def upload():
    data = UploadRequestSchema().load(request.get_json())
    # Decode and validate the base64 encoded file data
    file_data, mime = validate_file_data(data["file_data"])
    # Calculate the hash of the file data to use as the file name
    hash = hashlib.sha256(file_data).hexdigest()
    # Guess the mime of the file data to save the file with
    if not mime:
        mime = filetype.guess_mime(file_data)
    # Use a generic mime type if the guess failed
    if not mime:
        mime = "application/octet-stream"

    # Save the file with the correct extension if possible
    ext = filetype.get_type(mime=mime).extension
    path = ""
    if not ext or mime == "application/octet-stream":
        path = hash
    else:
        path = f"{hash}.{ext}"

    # Save the upload information to the database
    upload = Upload(path=path, mime=mime)
    try:
        db.session.add(upload)
        file = open(os.path.join(app.config["UPLOAD_FOLDER"], path), "wb")
        file.write(file_data)
        db.session.commit()
    # If the path is not unique, then an IntegrityError will be raised
    # This means that the file is already uploaded so we can just grab it
    # from the database
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        upload = Upload.query.filter_by(path=path).first()
    return {"message": "Upload successful!", "upload": UploadSchema().dump(upload)}, 201

@upload_bp.route("/<path:filename>", methods=["GET"])
def get_upload(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
