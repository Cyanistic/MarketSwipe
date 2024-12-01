from flask_jwt_extended import create_access_token
import pytest
from app import db, app
from auth import User, UserSchema
from support import SupportTicket


@pytest.fixture(scope="module")
def test_client():
    flask_app = app
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with flask_app.app_context():
        db.create_all()
        yield flask_app.test_client()
        db.drop_all()


@pytest.fixture(scope="module")
def new_user():
    user = User(email="test@example298134.com", password_hash="password")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope="module")
def access_token(new_user):
    return create_access_token(identity=UserSchema().dump(new_user))


def test_get_tickets_empty(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/api/support/tickets", headers=headers)
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_ticket(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"subject": "Test Subject", "description": "Test Description"}
    response = test_client.post(
        "/api/support/tickets/create", json=data, headers=headers
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Support ticket created successfully"
    assert "ticket_id" in data


def test_get_tickets(test_client, access_token, new_user):
    headers = {"Authorization": f"Bearer {access_token}"}

    # Use the ticket created in the previous test
    response = test_client.get("/api/support/tickets", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert isinstance(data, list)
    assert len(data) == 1
    ticket_data = data[0]
    assert ticket_data["subject"] == "Test Subject"
    assert ticket_data["description"] == "Test Description"


def test_get_ticket(test_client, access_token, new_user):
    headers = {"Authorization": f"Bearer {access_token}"}
    # Create a ticket first
    ticket = SupportTicket(
        user_id=new_user.id, subject="Test Subject", description="Test Description"
    )
    db.session.add(ticket)
    db.session.commit()

    response = test_client.get(f"/api/support/tickets/{ticket.id}", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["subject"] == "Test Subject"
    assert data["description"] == "Test Description"


def test_get_ticket_not_found(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/api/support/tickets/999", headers=headers)
    assert response.status_code == 404
    assert response.get_json() == {"message": "Support ticket not found"}


def test_create_ticket_missing_fields(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"subject": "Test Subject"}
    response = test_client.post(
        "/api/support/tickets/create", json=data, headers=headers
    )
    assert response.status_code == 400
    assert response.get_json() == {"message": "Subject and description are required"}
