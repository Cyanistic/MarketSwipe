import pytest
from flask_jwt_extended import create_access_token
from app import app, db
from auth import User, UserSchema
from cart import CartProduct
from products import Category, Product


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


@pytest.fixture(scope="module")
def headers(access_token):
    return {"Authorization": f"Bearer {access_token}"}


def test_get_cart_empty(test_client, headers):
    response = test_client.get("/api/cart/", headers=headers)
    assert response.status_code == 200
    assert response.get_json() == []


def test_add_cart_product(test_client, headers, new_user):
    category = Category(name="Furniture")
    product = Product(
        name="Test Product", price=10.0, category=category, seller_id=new_user.id
    )
    db.session.add(product)
    db.session.commit()

    response = test_client.post(
        "/api/cart/add", json={"productId": product.id, "quantity": 2}, headers=headers
    )
    assert response.status_code == 200
    assert response.get_json() == {"message": "Product successfully added to cart"}

    cart_product = CartProduct.query.filter_by(
        user_id=new_user.id, product_id=product.id
    ).first()
    assert cart_product is not None
    assert cart_product.quantity == 2


def test_remove_cart_product(test_client, headers, new_user):
    category = Category(name="Furnitures")
    product = Product(
        name="Test Produc2", price=10.0, category=category, seller_id=new_user.id
    )
    db.session.add(product)
    db.session.commit()

    cart_product = CartProduct(user_id=new_user.id, product_id=product.id, quantity=2)
    db.session.add(cart_product)
    db.session.commit()

    response = test_client.post(
        "/api/cart/remove", json={"productId": product.id}, headers=headers
    )
    assert response.status_code == 200
    assert response.get_json() == {"message": "Product successfully removed from cart"}

    cart_product = CartProduct.query.filter_by(
        user_id=new_user.id, product_id=product.id
    ).first()
    assert cart_product is None


def test_add_nonexistent_product(test_client, headers):
    response = test_client.post(
        "/api/cart/add", json={"productId": 999, "quantity": 2}, headers=headers
    )
    assert response.status_code == 404
    assert response.get_json() == {"message": "Product not found"}


def test_remove_nonexistent_product(test_client, headers):
    response = test_client.post(
        "/api/cart/remove", json={"productId": 999}, headers=headers
    )
    assert response.status_code == 403
    assert response.get_json() == {"message": "Product not in cart"}


def test_remove_without_product_id(test_client, headers):
    response = test_client.post("/api/cart/remove", json={}, headers=headers)
    assert response.status_code == 400
    assert response.get_json() == {"message": "productId is required"}
