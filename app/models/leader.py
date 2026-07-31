from app.extensions import db
from app.utils.mixins import TimestampMixin


class Leader(TimestampMixin, db.Model):
    __tablename__ = "leaders"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(150),
        nullable=False
    )

    position = db.Column(
        db.String(150),
        nullable=False
    )

    photo = db.Column(
        db.String(255),
        nullable=True
    )

    bio = db.Column(
        db.Text,
        nullable=True
    )

    email = db.Column(
        db.String(150),
        nullable=True
    )

    phone = db.Column(
        db.String(50),
        nullable=True
    )

    facebook = db.Column(
        db.String(255),
        nullable=True
    )

    twitter = db.Column(
        db.String(255),
        nullable=True
    )

    linkedin = db.Column(
        db.String(255),
        nullable=True
    )

    display_order = db.Column(
        db.Integer,
        default=1
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    def __repr__(self):
        return f"<Leader {self.name}>"