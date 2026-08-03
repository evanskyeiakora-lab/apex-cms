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


# ==========================================
# HOME
# ==========================================

@main_bp.route("/")
def home():

    slides = (
        HeroSlide.query
        .filter_by(is_active=True)
        .order_by(HeroSlide.display_order.asc())
        .all()
    )

    about_page = (
        Page.query
        .filter_by(
            slug="about",
            is_published=True
        )
        .first()
    )

    latest_news = (
        News.query
        .filter_by(status="published")
        .order_by(News.published_at.desc())
        .limit(3)
        .all()
    )

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

    leaders = (
        Leader.query
        .filter_by(is_active=True)
        .order_by(Leader.display_order.asc())
        .limit(8)
        .all()
    )

    stats = {
        "members_count": Member.query.count(),
        "leaders_count": Leader.query.count(),
        "news_count": News.query.count(),
        "events_count": Event.query.count(),
        "gallery_count": Gallery.query.count()
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


# ==========================================
# DYNAMIC PAGES
# ==========================================

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


# ==========================================
# NEWS
# ==========================================

@main_bp.route("/news")
def news():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    news_items = (
        News.query
        .filter_by(status="published")
        .order_by(News.published_at.desc())
        .paginate(
            page=page,
            per_page=9,
            error_out=False
        )
    )

    return render_template(
        "news/index.html",
        news_items=news_items
    )


# ==========================================
# NEWS DETAILS
# ==========================================

@main_bp.route("/news/<slug>")
def news_detail(slug):

    article = (
        News.query
        .filter_by(
            slug=slug,
            status="published"
        )
        .first_or_404()
    )

    related_news = (
        News.query
        .filter(
            News.status == "published",
            News.id != article.id
        )
        .order_by(News.published_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "news/detail.html",
        article=article,
        related_news=related_news
    )


# ==========================================
# EVENTS
# ==========================================

@main_bp.route("/events")
def events():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    events = (
        Event.query
        .filter(
            Event.is_published == True
        )
        .order_by(Event.start_date.asc())
        .paginate(
            page=page,
            per_page=9,
            error_out=False
        )
    )

    return render_template(
        "events/index.html",
        events=events
    )


# ==========================================
# EVENT DETAILS
# ==========================================

@main_bp.route("/events/<slug>")
def event_detail(slug):

    event = (
        Event.query
        .filter_by(
            slug=slug,
            is_published=True
        )
        .first_or_404()
    )

    related_events = (
        Event.query
        .filter(
            Event.is_published == True,
            Event.id != event.id
        )
        .order_by(Event.start_date.asc())
        .limit(3)
        .all()
    )

    return render_template(
        "events/detail.html",
        event=event,
        related_events=related_events
    )


# ==========================================
# GALLERY
# ==========================================

@main_bp.route("/gallery")
def gallery():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    galleries = (
        Gallery.query
        .filter_by(is_published=True)
        .order_by(
            Gallery.display_order.asc(),
            Gallery.created_at.desc()
        )
        .paginate(
            page=page,
            per_page=12,
            error_out=False
        )
    )

    return render_template(
        "gallery/index.html",
        galleries=galleries
    )


# ==========================================
# GALLERY DETAILS
# ==========================================

@main_bp.route("/gallery/<slug>")
def gallery_detail(slug):

    gallery = (
        Gallery.query
        .filter_by(
            slug=slug,
            is_published=True
        )
        .first_or_404()
    )

    related_images = (
        Gallery.query
        .filter(
            Gallery.is_published == True,
            Gallery.category == gallery.category,
            Gallery.id != gallery.id
        )
        .order_by(
            Gallery.created_at.desc()
        )
        .limit(6)
        .all()
    )

    return render_template(
        "gallery/detail.html",
        gallery=gallery,
        related_images=related_images
    )