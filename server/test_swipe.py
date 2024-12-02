from flask_jwt_extended import create_access_token
import pytest
from app import db, app
from auth import User, UserSchema
from products import Category, Product, SwipeHistory, Tag


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


def create_test_data():
    user = User.query.first()
    category_electronics = Category(name='Electronics')
    category_fashion = Category(name='Fashion')
    category_home = Category(name='Home')
    category_sports = Category(name='Sports')
    category_books = Category(name='Books')
    
    tag_black = Tag(name='Black')
    tag_white = Tag(name='White')
    tag_large = Tag(name='Large')
    tag_small = Tag(name='Small')
    tag_nike = Tag(name='Nike')
    tag_apple = Tag(name='Apple')
    
    product1 = Product(name='Smartphone', price=699.99, category=category_electronics, seller_id=user.id)
    product2 = Product(name='Laptop', price=999.99, category=category_electronics, seller_id=user.id)
    product3 = Product(name='T-shirt', price=19.99, category=category_fashion, seller_id=user.id)
    product4 = Product(name='Jeans', price=49.99, category=category_fashion, seller_id=user.id)
    product5 = Product(name='Sofa', price=499.99, category=category_home, seller_id=user.id)
    product6 = Product(name='Coffee Table', price=199.99, category=category_home, seller_id=user.id)
    product7 = Product(name='Basketball', price=29.99, category=category_sports, seller_id=user.id)
    product8 = Product(name='Tennis Racket', price=89.99, category=category_sports, seller_id=user.id)
    product9 = Product(name='Novel', price=14.99, category=category_books, seller_id=user.id)
    product10 = Product(name='Cookbook', price=24.99, category=category_books, seller_id=user.id)
    
    db.session.add_all([category_electronics, category_fashion, category_home, category_sports, category_books,
                        tag_black, tag_white, tag_large, tag_small, tag_nike, tag_apple,
                        product1, product2, product3, product4, product5, product6, product7, product8, product9, product10])
    db.session.commit()
    
    product1.tags.extend([tag_black, tag_apple])
    product2.tags.extend([tag_white, tag_apple])
    product3.tags.extend([tag_black, tag_nike])
    product4.tags.extend([tag_large, tag_nike])
    product5.tags.extend([tag_large])
    product6.tags.extend([tag_small])
    product7.tags.extend([tag_large, tag_nike])
    product8.tags.extend([tag_small, tag_nike])
    product9.tags.extend([tag_black])
    product10.tags.extend([tag_white])
    
    db.session.commit()

def test_swipe_and_recommend(test_client, access_token):
    create_test_data()
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Swipe right (like) on Smartphone
    response = test_client.post('/api/products/swipe', json={'product_id': 1, 'liked': True}, headers=headers)
    assert response.status_code == 200
    assert response.get_json()['name'] in ['Laptop']
    
    # Swipe left (dislike) on Laptop
    response = test_client.post('/api/products/swipe', json={'product_id': 2, 'liked': False}, headers=headers)
    assert response.status_code == 200
    assert response.get_json()['name'] not in ['Laptop']
    
    # Swipe right (like) on T-shirt
    response = test_client.post('/api/products/swipe', json={'product_id': 3, 'liked': True}, headers=headers)
    assert response.status_code == 200
    assert response.get_json()['name'] in ['Jeans']
    
    # Swipe left (dislike) on Jeans
    response = test_client.post('/api/products/swipe', json={'product_id': 4, 'liked': False}, headers=headers)
    assert response.status_code == 200
    assert response.get_json()['name'] not in ['Jeans']
    
    # Swipe right (like) on Sofa
    response = test_client.post('/api/products/swipe', json={'product_id': 5, 'liked': True}, headers=headers)
    assert response.status_code == 200
    assert response.get_json()['name'] in ['Coffee Table']
    
    # Swipe left (dislike) on Coffee Table
    response = test_client.post('/api/products/swipe', json={'product_id': 6, 'liked': False}, headers=headers)
    assert response.status_code == 200
    assert response.get_json()['name'] not in ['Coffee Table']
    
    # Swipe right (like) on Basketball
    response = test_client.post('/api/products/swipe', json={'product_id': 7, 'liked': True}, headers=headers)
    assert response.status_code == 200
    assert response.get_json()['name'] in ['Tennis Racket']
    
    # Swipe left (dislike) on Tennis Racket
    response = test_client.post('/api/products/swipe', json={'product_id': 8, 'liked': False}, headers=headers)
    assert response.status_code == 200
    assert response.get_json()['name'] not in ['Tennis Racket']
    
    # Swipe right (like) on Novel
    response = test_client.post('/api/products/swipe', json={'product_id': 9, 'liked': True}, headers=headers)
    assert response.status_code == 200
    assert response.get_json()['name'] in ['Cookbook']
    
    # Swipe left (dislike) on Cookbook
    response = test_client.post('/api/products/swipe', json={'product_id': 10, 'liked': False}, headers=headers)
    assert response.status_code == 200
    assert response.get_json()['name'] in ['Novel']

def test_reset_category_swipe_history(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    # Swipe right (like) on Smartphone
    test_client.post('/api/products/swipe', json={'product_id': 1, 'liked': True}, headers=headers)
    # Swipe right (like) on T-shirt
    test_client.post('/api/products/swipe', json={'product_id': 3, 'liked': True}, headers=headers)
    
    # Reset swipe history for Electronics category
    response = test_client.post('/api/products/reset/1', headers=headers)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Swipe history for category 1 reset successfully'
    
    # Verify swipe history for Electronics category is empty
    swipe_history = SwipeHistory.query.join(Product, SwipeHistory.product_id == Product.id) \
        .filter(SwipeHistory.user_id == 1, Product.category_id == 1).all()
    assert len(swipe_history) == 0
    
    # Verify swipe history for other categories is not affected
    swipe_history = SwipeHistory.query.join(Product, SwipeHistory.product_id == Product.id) \
        .filter(SwipeHistory.user_id == 1).all()
    assert len(swipe_history) > 0

def test_reset_all_swipe_history(test_client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    # Swipe right (like) on Smartphone
    test_client.post('/api/products/swipe', json={'product_id': 1, 'liked': True}, headers=headers)
    
    # Reset all swipe history
    response = test_client.post('/api/products/reset', headers=headers)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'All swipe history reset successfully'
    
    # Verify swipe history is empty
    swipe_history = SwipeHistory.query.filter_by(user_id=1).all()
    assert len(swipe_history) == 0

