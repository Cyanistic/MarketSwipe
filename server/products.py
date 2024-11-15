from app import SQLAlchemyAutoCamelCaseSchema, db, ma
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from auth import User

products_bp = Blueprint("product", __name__, url_prefix='/products')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", backref="category")
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    modified_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

class SwipeHistory(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False, primary_key=True)
    user = db.relationship("User", backref="user")
    product = db.relationship("Product", backref="product")
    liked = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

# Schemas for serialization/deserialization
class ProductSchema(SQLAlchemyAutoCamelCaseSchema):
    Category = ma.Nested('CategorySchema')
    class Meta:
        model = Product

class CategorySchema(SQLAlchemyAutoCamelCaseSchema):
    class Meta:
        model = Category

class TagSchema(SQLAlchemyAutoCamelCaseSchema):
    class Meta:
        model = Tag

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
tag_schema = TagSchema()
tags_schema = TagSchema(many=True)

# Product CRUD Endpoints

# CREATE Product
@products_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        price=data['price'],
        category_id=data['category_id']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created successfully", "product": product_schema.dump(new_product)}), 201

# READ all Products
@products_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify(products_schema.dump(products)), 200

# READ single Product by ID
@products_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product_schema.dump(product)), 200

# UPDATE Product
@products_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get_or_404(id)
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.category_id = data.get('category_id', product.category_id)
    db.session.commit()
    return jsonify({"message": "Product updated successfully", "product": product_schema.dump(product)}), 200

# DELETE Product
@products_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200

# Category CRUD Endpoints

# CREATE Category
@products_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(name=data['name'], description=data.get('description'))
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Category created successfully", "category": category_schema.dump(new_category)}), 201

# READ all Categories
@products_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify(categories_schema.dump(categories)), 200

# DELETE Category
@products_bp.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted successfully"}), 200

# Tag CRUD Endpoints

# CREATE Tag
@products_bp.route('/tags', methods=['POST'])
def create_tag():
    data = request.get_json()
    new_tag = Tag(name=data['name'])
    db.session.add(new_tag)
    db.session.commit()
    return jsonify({"message": "Tag created successfully", "tag": tag_schema.dump(new_tag)}), 201

# READ all Tags
@products_bp.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify(tags_schema.dump(tags)), 200

