from app.extensions import db
from app.utils.mixins import TimestampMixin


class HeroSlide(TimestampMixin, db.Model):
    __tablename__ = "hero_slides"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    subtitle = db.Column(
        db.Text,
        nullable=True
    )

    image = db.Column(
        db.String(255),
        nullable=False
    )

    button_text = db.Column(
        db.String(100),
        nullable=True
    )

    button_url = db.Column(
        db.String(255),
        nullable=True
    )

    display_order = db.Column(
        db.Integer,
        default=1
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    def __repr__(self):
        return f"<HeroSlide {self.title}>"