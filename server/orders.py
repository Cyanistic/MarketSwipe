from app import db, ma
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="orders")
    total = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

class Order_Items(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False, primary_key=True)
    order = db.relationship("Orders", backref="order_items")
    product = db.relationship("Product", backref="order_items")
    quantity = db.Column(db.Integer, nullable=False, default=1)
    item_cost = db.Column(db.Numeric(10, 2), nullable=False)

class Payment(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)
    order = db.relationship("Orders", backref="payment")
    user = db.relationship("User", backref="payment")
    payment_method = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

class Order_History(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, primary_key=True)
    user = db.relationship("User", backref="order_history")
    order = db.relationship("Orders", backref="order_history")
    total = db.Column(db.Numeric(10, 2), nullable=False)
    current_status = db.Column(db.String(20), nullable=False)
    purchase_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    last_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc), 
        onupdate=datetime.now(timezone.utc)
    )

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")
