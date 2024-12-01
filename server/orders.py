from flask_jwt_extended import current_user, jwt_manager
from flask_jwt_extended.view_decorators import jwt_required
from marshmallow.fields import Nested
from app import SQLAlchemyAutoCamelCaseSchema, db, ma
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request

from cart import CartProduct


orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="order")
    total = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )


class OrderItem(db.Model):
    order_id = db.Column(
        db.Integer, db.ForeignKey("order.id"), nullable=False, primary_key=True
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=False, primary_key=True
    )
    order = db.relationship("Order", backref="order_item")
    product = db.relationship("Product", backref="order_item")
    quantity = db.Column(db.Integer, nullable=False, default=1)


class Payment(db.Model):
    order_id = db.Column(
        db.Integer, db.ForeignKey("order.id"), nullable=False, primary_key=True
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True
    )
    order = db.relationship("Order", backref="payment")
    user = db.relationship("User", backref="payment")
    payment_method = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )


class OrderSchema(SQLAlchemyAutoCamelCaseSchema):
    class Meta:
        model = Order
        include_fk = True
        load_instance = True


@orders_bp.route("/", methods=["GET"])
@jwt_required()
def get_orders():
    """
    Retrieve all orders for the logged-in user.

    Returns:
        JSON response containing a list of orders or a message if no orders are found.
    """
    user_id = current_user.id
    orders = Order.query.filter_by(user_id=user_id).all()
    orders_list = [
        {
            "id": order.id,
            "total": order.total,
            "status": order.status,
            "created_at": order.created_at.isoformat(),
            "items": [
                {"product_id": item.product_id, "quantity": item.quantity}
                for item in OrderItem.query.filter_by(order_id=order.id).all()
            ],
        }
        for order in orders
    ]
    return jsonify(orders_list), 200


@orders_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id):
    """
    Retrieve details of a specific order by its ID for the logged-in user.

    Args:
        order_id (int): The ID of the order to retrieve.

    Returns:
        JSON response containing the order details or a message if the order is not found.
    """
    user_id = current_user.id
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({"message": "Order not found"}), 404
    order_details = {
        "id": order.id,
        "total": order.total,
        "status": order.status,
        "created_at": order.created_at.isoformat(),
        "items": [
            {"product_id": item.product_id, "quantity": item.quantity}
            for item in OrderItem.query.filter_by(order_id=order.id).all()
        ],
    }
    return jsonify(order_details), 200


@orders_bp.route("/create", methods=["POST"])
@jwt_required()
def create_order():
    """
    Create a new order for the logged-in user by taking items from the user's cart.

    Returns:
        JSON response containing a success message and the order ID, or an error message if the cart is empty.
    """
    user_id = current_user.id
    cart_items = CartProduct.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    total = sum(item.product.price * item.quantity for item in cart_items)

    new_order = Order(user_id=user_id, total=total, status="pending")
    db.session.add(new_order)
    db.session.commit()

    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
        )
        db.session.add(order_item)
        db.session.delete(cart_item)  # Remove item from cart after adding to order

    db.session.commit()

    return (
        jsonify({"message": "Order created successfully", "order_id": new_order.id}),
        201,
    )
