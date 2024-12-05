import pytest
from app import app, db
from flask_jwt_extended import create_access_token
from products import Product, Category, Tag
from auth import User, UserSchema

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
    user = User(email="test@example.com", password_hash="password")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture(scope="module")
def access_token(new_user):
    return create_access_token(identity=UserSchema().dump(new_user))

def test_create_product(test_client, access_token):
    category = Category(name="Electronics")
    db.session.add(category)
    db.session.commit()

    response = test_client.post(
        "/api/products/",
        json={"name": "Laptop", "price": 999.99, "categoryId": category.id},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 201
    assert response.json["message"] == "Product created successfully"
    assert response.json["product"]["name"] == "Laptop"

def test_get_products(test_client):
    response = test_client.get("/api/products/")
    assert response.status_code == 200
    assert len(response.json) > 0

def test_get_product(test_client):
    product = Product.query.first()
    response = test_client.get(f"/api/products/{product.id}")
    assert response.status_code == 200
    assert response.json["name"] == product.name


def test_create_tag(test_client):
    response = test_client.post("/api/products/tags", json={"name": "New Tag"})
    assert response.status_code == 201
    assert response.json["message"] == "Tag created successfully"
    assert response.json["tag"]["name"] == "New Tag"

def test_update_product(test_client, access_token):
    product = Product.query.first()
    response = test_client.put(
        f"/api/products/{product.id}",
        json={"name": "Updated Laptop", "price": 1099.99, "tags": ["New Tag"]},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json["message"] == "Product updated successfully"
    assert response.json["product"]["name"] == "Updated Laptop"

def test_delete_product(test_client, access_token):
    product = Product.query.first()
    response = test_client.delete(
        f"/api/products/{product.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json["message"] == "Product deleted successfully"

def test_create_category(test_client):
    response = test_client.post(
        "/api/products/categories",
        json={"name": "Books", "description": "All kinds of books"},
    )
    assert response.status_code == 201
    assert response.json["message"] == "Category created successfully"
    assert response.json["category"]["name"] == "Books"

def test_get_categories(test_client):
    response = test_client.get("/api/products/categories")
    assert response.status_code == 200
    assert len(response.json) > 0

def test_delete_category(test_client):
    category = Category.query.first()
    response = test_client.delete(f"/api/products/categories/{category.id}")
    assert response.status_code == 200
    assert response.json["message"] == "Category deleted successfully"
