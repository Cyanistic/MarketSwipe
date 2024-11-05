from app import db, ma
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="order")
    total = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

class OrderItem(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False, primary_key=True)
    order = db.relationship("Order", backref="order_item")
    product = db.relationship("Product", backref="order_item")
    quantity = db.Column(db.Integer, nullable=False, default=1)

class Payment(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)
    order = db.relationship("Order", backref="payment")
    user = db.relationship("User", backref="payment")
    payment_method = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")
