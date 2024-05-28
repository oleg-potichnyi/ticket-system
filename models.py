from datetime import datetime
from flask_login import UserMixin
from app import db


class TicketStatus:
    PENDING = "Pending"
    IN_REVIEW = "In review"
    CLOSED = "Closed"
    choices = [PENDING, IN_REVIEW, CLOSED]


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(
        db.Enum(*TicketStatus.choices, name="ticket_status"),
        default=TicketStatus.PENDING,
        nullable=False,
    )
    note = db.Column(db.Text, nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class UserRole:
    ADMIN = "Admin"
    MANAGER = "Manager"
    ANALYST = "Analyst"
    choices = [ADMIN, MANAGER, ANALYST]


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=True)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
