from datetime import datetime

from app.extensions import db
from slugify import slugify

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    slug = db.Column(
        db.String(200),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    featured_image = db.Column(
        db.String(255)
    )

    venue = db.Column(
        db.String(255)
    )

    start_date = db.Column(
        db.Date,
        nullable=False
    )

    end_date = db.Column(
        db.Date
    )

    start_time = db.Column(
        db.Time
    )

    end_time = db.Column(
        db.Time
    )

    organizer = db.Column(
        db.String(255)
    )

    registration_link = db.Column(
        db.String(500)
    )

    display_order = db.Column(
        db.Integer,
        default=0
    )

    is_featured = db.Column(
        db.Boolean,
        default=False
    )

    is_published = db.Column(
        db.Boolean,
        default=True
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
    
  

def generate_slug(self):
    base_slug = slugify(self.title)
    slug = base_slug
    counter = 1

    while Event.query.filter(
        Event.slug == slug,
        Event.id != self.id
    ).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    self.slug = slug