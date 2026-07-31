from app.extensions import db
from app.models.mixins import TimestampMixin, PublishMixin
from app.utils.slug import generate_unique_slug


class Gallery(
    TimestampMixin,
    PublishMixin,
    db.Model
):
    __tablename__ = "gallery"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    slug = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    image = db.Column(
        db.String(255),
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False,
        default="General",
        index=True
    )

    display_order = db.Column(
        db.Integer,
        nullable=False,
        default=0,
        index=True
    )

    is_featured = db.Column(
        db.Boolean,
        default=False,
        index=True
    )

    def generate_slug(self):
        self.slug = generate_unique_slug(
            Gallery,
            self.title
        )

    @property
    def image_url(self):
        if self.image:
            return f"uploads/gallery/{self.image}"
        return "images/no-image.jpg"

    def __repr__(self):
        return f"<Gallery {self.title}>"