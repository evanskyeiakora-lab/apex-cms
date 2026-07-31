from slugify import slugify

from app.extensions import db
from app.utils.mixins import (
    TimestampMixin,
    PublishMixin,
)


class News(TimestampMixin, PublishMixin, db.Model):
    __tablename__ = "news"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    slug = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    featured_image = db.Column(
        db.String(255)
    )

    def generate_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1

        while News.query.filter(
            News.slug == slug,
            News.id != self.id
        ).first():

            slug = f"{base_slug}-{counter}"
            counter += 1

        self.slug = slug

    def publish(self):
        from datetime import datetime

        self.status = "published"

        if not self.published_at:
            self.published_at = datetime.utcnow()

    def __repr__(self):
        return f"<News {self.title}>"