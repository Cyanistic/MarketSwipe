import pytest
from app import app, db
from flask_jwt_extended import create_access_token
from cart import CartProduct
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


def test_get_orders_empty(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/api/orders/", headers=headers)
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_order(test_client, access_token, new_user):
    headers = {"Authorization": f"Bearer {access_token}"}

    # Add categories and products to the database
    category1 = Category(name="Category 1")
    category2 = Category(name="Category 2")
    db.session.add(category1)
    db.session.add(category2)
    db.session.commit()

    product1 = Product(
        name="Product 1", price=10.0, category_id=category1.id, seller=new_user
    )
    product2 = Product(
        name="Product 2", price=20.0, category_id=category2.id, seller=new_user
    )
    db.session.add(product1)
    db.session.add(product2)
    db.session.commit()

    # Add products to the cart
    cart_item1 = CartProduct(user_id=new_user.id, product_id=product1.id, quantity=1)
    cart_item2 = CartProduct(user_id=new_user.id, product_id=product2.id, quantity=2)
    db.session.add(cart_item1)
    db.session.add(cart_item2)
    db.session.commit()

    response = test_client.post("/api/orders/create", headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Order created successfully"
    assert "order_id" in data


def test_get_orders(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/api/orders/", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    order = data[0]
    assert order["total"] == "50.00"
    assert order["status"] == "pending"
    assert len(order["items"]) == 2


def test_get_order(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/api/orders/1", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["total"] == "50.00"
    assert data["status"] == "pending"
    assert len(data["items"]) == 2


def test_get_nonexistent_order(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/api/orders/999", headers=headers)
    assert response.status_code == 404
    assert response.get_json() == {"message": "Order not found"}
