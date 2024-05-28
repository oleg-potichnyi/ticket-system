from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == UserRole.ADMIN

    def is_manager(self):
        return self.role == UserRole.MANAGER

    def is_analyst(self):
        return self.role == UserRole.ANALYST


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    users = db.relationship('User', backref='group', lazy=True)
    tickets = db.relationship('Ticket', backref='group', lazy=True)
