from flask_jwt_extended import jwt_required, current_user
from marshmallow import EXCLUDE, fields
from app import CamelCaseSchema, SQLAlchemyAutoCamelCaseSchema, db, ma
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from auth import User

products_bp = Blueprint("product", __name__, url_prefix="/products")


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
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    seller = db.relationship("User", backref="product")
    category = db.relationship("Category", backref="product")
    tags = db.relationship('Tag', secondary='product_tag', backref='products')
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    modified_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )


class ProductTag(db.Model):
    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), primary_key=True, nullable=False
    )
    tag_id = db.Column(
        db.Integer, db.ForeignKey("tag.id"), primary_key=True, nullable=False
    )
    # tag = db.relationship("Tag", backref="product_tag")
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )


class SwipeHistory(db.Model):
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=False, primary_key=True
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id"), nullable=False
    )
    user = db.relationship("User", backref="swipe_history")
    product = db.relationship("Product", backref="swipe_history")
    category = db.relationship("Category", backref="swipe_history")
    liked = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )


# Schemas for serialization/deserialization
class ProductSchema(SQLAlchemyAutoCamelCaseSchema):
    Category = ma.Nested("CategorySchema")

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


class CreateProductSchema(CamelCaseSchema):
    name = fields.String(required=True)
    price = fields.Float(required=True)
    category_id = fields.Integer(required=True)

    class Meta:
        unknown = EXCLUDE


# CREATE Product
@products_bp.route("/", methods=["POST"])
@jwt_required()
def create_product():
    data = CreateProductSchema().load(request.get_json())
    new_product = Product(
        name=data["name"],
        price=data["price"],
        category_id=data["category_id"],
        seller_id=current_user.id,
    )
    db.session.add(new_product)
    db.session.commit()
    return (
        jsonify(
            {
                "message": "Product created successfully",
                "product": product_schema.dump(new_product),
            }
        ),
        201,
    )


# READ all Products
@products_bp.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify(products_schema.dump(products)), 200


# READ single Product by ID
@products_bp.route("/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product_schema.dump(product)), 200


# Get all uploads associated with a product
@products_bp.route("/<int:id>/uploads", methods=["GET"])
def get_product_uploads(id):
    from upload import ProductUpload, Upload, UploadSchema

    product_uploads_schema = UploadSchema(many=True)
    product_uploads = (
        Upload.query.join(ProductUpload, ProductUpload.upload_id == Upload.id)
        .filter_by(product_id=id)
        .all()
    )
    return jsonify(product_uploads_schema.dump(product_uploads)), 200


# UPDATE Product
@products_bp.route("/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.get_json()
    product = Product.query.get_or_404(id)
    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.category_id = data.get("category_id", product.category_id)
    db.session.commit()
    return (
        jsonify(
            {
                "message": "Product updated successfully",
                "product": product_schema.dump(product),
            }
        ),
        200,
    )


# DELETE Product
@products_bp.route("/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200


# Category CRUD Endpoints


# CREATE Category
@products_bp.route("/categories", methods=["POST"])
def create_category():
    data = request.get_json()
    new_category = Category(name=data["name"], description=data.get("description"))
    db.session.add(new_category)
    db.session.commit()
    return (
        jsonify(
            {
                "message": "Category created successfully",
                "category": category_schema.dump(new_category),
            }
        ),
        201,
    )


# READ all Categories
@products_bp.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify(categories_schema.dump(categories)), 200


# DELETE Category
@products_bp.route("/categories/<int:id>", methods=["DELETE"])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted successfully"}), 200


# Tag CRUD Endpoints


# CREATE Tag
@products_bp.route("/tags", methods=["POST"])
def create_tag():
    data = request.get_json()
    new_tag = Tag(name=data["name"])
    db.session.add(new_tag)
    db.session.commit()
    return (
        jsonify(
            {"message": "Tag created successfully", "tag": tag_schema.dump(new_tag)}
        ),
        201,
    )


# READ all Tags
@products_bp.route("/tags", methods=["GET"])
def get_tags():
    tags = Tag.query.all()
    return jsonify(tags_schema.dump(tags)), 200


@products_bp.route("/swipe", methods=["POST"])
@jwt_required()
def record_swipe_and_recommend():
    data = request.get_json()
    product_id = data["product_id"]
    liked = data["liked"]
    
    # Get the category of the swiped product
    swiped_product = Product.query.get(product_id)
    category_id = swiped_product.category_id
    
    # Check if the swipe history already exists
    swipe_history = SwipeHistory.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if swipe_history:
        # Update the existing swipe history
        swipe_history.liked = liked
        swipe_history.created_at = datetime.now(timezone.utc)
    else:
        # Create a new swipe history record
        swipe_history = SwipeHistory(
            user_id=current_user.id,
            product_id=product_id,
            category_id=category_id,  # Store category_id
            liked=liked
        )
        db.session.add(swipe_history)
    
    db.session.commit()
    
    # Get the category of the swiped product
    swiped_product = db.session.get(Product, product_id)
    category_id = swiped_product.category_id
    
    # Get all swipe history for the user within the same category
    user_swipe_history = (
        db.session.query(SwipeHistory)
        .join(Product, SwipeHistory.product_id == Product.id)
        .filter(SwipeHistory.user_id == current_user.id, Product.category_id == category_id)
        .order_by(SwipeHistory.created_at.desc())
        .all()
    )
    
    # Calculate tag weights based on swipe history within the same category
    tag_weights = {}
    for i, swipe in enumerate(user_swipe_history):
        weight = 1 / (i + 1)  # Recent swipes have more weight
        product = db.session.get(Product, swipe.product_id)
        for tag in product.tags:
            if tag.id not in tag_weights:
                tag_weights[tag.id] = 0
            tag_weights[tag.id] += weight if swipe.liked else -weight
    
    # Score products based on tag weights within the same category
    products = Product.query.filter_by(category_id=category_id).all()
    product_scores = []
    for product in products:
        if product.id == product_id:
            continue  # Skip the current product
        score = sum(tag_weights.get(tag.id, 0) for tag in product.tags)
        product_scores.append((product, score))
    
    # Sort products by score in descending order
    product_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Recommend the product with the highest score
    if product_scores:
        recommended_product = product_scores[0][0]
        return jsonify(product_schema.dump(recommended_product)), 200
    else:
        return jsonify({"message": "No more products to recommend based on your preferences"}), 200

# Reset all swipe history for the current user
@products_bp.route("/reset", methods=["POST"])
@jwt_required()
def reset_all_swipe_history():
    SwipeHistory.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({"message": "All swipe history reset successfully"}), 200

# Reset swipe history for a given category for the current user
@products_bp.route("/reset/<int:category_id>", methods=["POST"])
@jwt_required()
def reset_category_swipe_history(category_id):
    swipe_histories = SwipeHistory.query.join(Product, SwipeHistory.product_id == Product.id) \
        .filter(SwipeHistory.user_id == current_user.id, Product.category_id == category_id).all()
    
    for swipe_history in swipe_histories:
        db.session.delete(swipe_history)
    
    db.session.commit()
    return jsonify({"message": f"Swipe history for category {category_id} reset successfully"}), 200


