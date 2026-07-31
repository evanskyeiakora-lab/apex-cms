from flask import render_template

from app import db
from app.models import (
    Settings,
    HeroSlide,
    News,
    Event,
    Gallery,
    Member
)

from . import main_bp


# ==========================================
# Home
# ==========================================

@main_bp.route("/")
def index():

    settings = Settings.query.first()

    hero_slides = (
        HeroSlide.query
        .filter_by(is_published=True)
        .order_by(HeroSlide.display_order.asc())
        .all()
    )

    latest_news = (
        News.query
        .filter_by(is_published=True)
        .order_by(News.created_at.desc())
        .limit(3)
        .all()
    )

    upcoming_events = (
        Event.query
        .filter_by(is_published=True)
        .order_by(Event.event_date.asc())
        .limit(3)
        .all()
    )

    gallery = (
        Gallery.query
        .filter_by(is_published=True)
        .order_by(Gallery.created_at.desc())
        .limit(8)
        .all()
    )

    leaders = (
        Member.query
        .filter_by(is_published=True)
        .order_by(Member.display_order.asc())
        .limit(8)
        .all()
    )

    return render_template(
        "index.html",
        settings=settings,
        hero_slides=hero_slides,
        latest_news=latest_news,
        upcoming_events=upcoming_events,
        gallery=gallery,
        leaders=leaders,
    )


# ==========================================
# About
# ==========================================

@main_bp.route("/about")
def about():
    return render_template("about.html")


# ==========================================
# Contact
# ==========================================

@main_bp.route("/contact")
def contact():
    return render_template("contact.html")

    from app.models import Settings

@main_bp.route("/")
def index():

    settings = Settings.query.first()

    print("PUBLIC SITE SETTINGS")
    print(settings.id)
    print(settings.site_name)

    return render_template(
        "index.html",
        settings=settings,
        # ...
    )