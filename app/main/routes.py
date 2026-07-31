from datetime import date

from flask import (
    render_template,
    request
)

from . import main_bp

from app.models import (
    News,
    HeroSlide,
    Page,
    Event,
    Gallery,
    Leader,
    Member
)



# ======================================
# Home
# ======================================

@main_bp.route("/")
def home():

    # Hero Slider
    slides = (
        HeroSlide.query
        .filter_by(is_active=True)
        .order_by(HeroSlide.display_order.asc())
        .all()
    )

    # About Page
    about_page = (
        Page.query
        .filter_by(
            slug="about",
            is_published=True
        )
        .first()
    )

    # Latest News
    latest_news = (
        News.query
        .filter_by(status="published")
        .order_by(News.published_at.desc())
        .limit(3)
        .all()
    )

    # Upcoming Events
    upcoming_events = (
        Event.query
        .filter(
            Event.is_published == True,
            Event.start_date >= date.today()
        )
        .order_by(Event.start_date.asc())
        .limit(3)
        .all()
    )

    # Featured Gallery
    featured_gallery = (
        Gallery.query
        .filter_by(
            is_published=True,
            is_featured=True
        )
        .order_by(
            Gallery.display_order.asc(),
            Gallery.created_at.desc()
        )
        .limit(8)
        .all()
    )

    # Active Leaders
    leaders = (
        Leader.query
        .filter_by(is_active=True)
        .order_by(Leader.display_order.asc())
        .limit(8)
        .all()
    )

    # Website Statistics
    stats = {
        "members_count": Member.query.count(),
        "news_count": News.query.count(),
        "events_count": Event.query.count(),
        "gallery_count": Gallery.query.count(),
        "leaders_count": Leader.query.count()
    }

    return render_template(
        "index.html",
        slides=slides,
        about_page=about_page,
        latest_news=latest_news,
        upcoming_events=upcoming_events,
        featured_gallery=featured_gallery,
        leaders=leaders,
        stats=stats
    )

    # ======================================
# Dynamic Pages
# ======================================

@main_bp.route("/page/<slug>")
def page(slug):

    page = (
        Page.query
        .filter_by(
            slug=slug,
            is_published=True
        )
        .first_or_404()
    )

    return render_template(
        "page.html",
        page=page
    )