from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        index=True
    )

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    phone = db.Column(
        db.String(30)
    )

    photo = db.Column(
        db.String(255)
    )

    role = db.Column(
        db.String(30),
        nullable=False,
        default="Administrator",
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    last_login = db.Column(
        db.DateTime
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_super_admin(self):
        return self.role == "Super Admin"

    @property
    def is_admin(self):
        return self.role in [
            "Super Admin",
            "Administrator"
        ]

    def __repr__(self):
        return f"<User {self.username}>"