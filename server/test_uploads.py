import pytest
from flask_jwt_extended import create_access_token
from auth import User, UserSchema
from upload import upload_bp, Upload, validate_file_data
from app import app, db
import base64

@pytest.fixture(scope="module")
def test_client():
   flask_app = app
   flask_app.config["TESTING"] = True
   flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
   flask_app.config["UPLOAD_FOLDER"] = "/tmp/uploads"

   with flask_app.app_context():
       db.create_all()
       yield flask_app.test_client()
       db.drop_all()

@pytest.fixture(scope="module")
def new_user():
    user = User(email="test@example.com", password_hash="password")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture(scope="module")
def access_token(new_user):
    return create_access_token(identity=UserSchema().dump(new_user))

def test_upload_file(test_client, access_token):
    file_data = base64.b64encode(b"test file content").decode("utf-8")
    response = test_client.post(
        "/api/upload/",
        json={"fileData": f"data:text/plain;base64,{file_data}"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Upload successful!"
    assert "upload" in data

def test_get_upload(test_client, access_token):
    file_data = base64.b64encode(b"test file content").decode("utf-8")
    response = test_client.post(
        "/api/upload/",
        json={"fileData": f"data:text/plain;base64,{file_data}"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 201
    data = response.get_json()
    filename = data["upload"]["path"]

    response = test_client.get(f"/api/upload/{filename}")
    assert response.status_code == 200

def test_validate_file_data():
    file_data = base64.b64encode(b"test file content").decode("utf-8")
    decoded_data, mime = validate_file_data(f"data:text/plain;base64,{file_data}")
    assert decoded_data == b"test file content"
    assert mime == "text/plain"

def test_validate_file_data_no_mime():
    file_data = base64.b64encode(b"test file content").decode("utf-8")
    decoded_data, mime = validate_file_data(file_data)
    assert decoded_data == b"test file content"
    assert mime is None
