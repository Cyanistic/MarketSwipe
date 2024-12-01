from flask_jwt_extended import current_user, jwt_required
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from app import SQLAlchemyAutoCamelCaseSchema, db

support_bp = Blueprint("support", __name__, url_prefix="/support")


class SupportTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="support_ticket")
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="open")
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )


class SupportTicketSchema(SQLAlchemyAutoCamelCaseSchema):
    class Meta:
        model = SupportTicket
        include_fk = True
        load_instance = True


@support_bp.route("/tickets", methods=["GET"])
@jwt_required()
def get_tickets():
    """
    Retrieve all support tickets for the logged-in user.

    Returns:
        JSON response containing a list of support tickets or a message if no tickets are found.
    """
    user_id = current_user.id
    tickets = SupportTicket.query.filter_by(user_id=user_id).all()
    return jsonify(SupportTicketSchema().dump(tickets, many=True)), 200


@support_bp.route("/tickets/<int:ticket_id>", methods=["GET"])
@jwt_required()
def get_ticket(ticket_id):
    """
    Retrieve details of a specific support ticket by its ID for the logged-in user.

    Args:
        ticket_id (int): The ID of the support ticket to retrieve.

    Returns:
        JSON response containing the support ticket details or a message if the ticket is not found.
    """
    user_id = current_user.id
    ticket = SupportTicket.query.filter_by(id=ticket_id).first()
    if not ticket:
        return jsonify({"message": "Support ticket not found"}), 404
    if not ticket.user_id == user_id:
        return jsonify({"message": "You are not authorized to view this ticket"}), 403
    return jsonify(SupportTicketSchema().dump(ticket)), 200


@support_bp.route("/tickets/create", methods=["POST"])
@jwt_required()
def create_ticket():
    """
    Create a new support ticket for the logged-in user.

    Returns:
        JSON response containing a success message and the ticket ID, or an error message if the request is invalid.
    """
    user_id = current_user.id
    data = request.get_json()
    subject = data.get("subject")
    description = data.get("description")

    if not subject or not description:
        return jsonify({"message": "Subject and description are required"}), 400

    new_ticket = SupportTicket(
        user_id=user_id, subject=subject, description=description, status="open"
    )
    db.session.add(new_ticket)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Support ticket created successfully",
                "ticket_id": new_ticket.id,
            }
        ),
        201,
    )
