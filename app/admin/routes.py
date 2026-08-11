from flask import render_template
from flask_login import login_required

from . import admin_bp

from app.models import (
    User,
    News,
    Gallery,
    Member,
    ContactMessage,
    HeroSlide,
    Page,
    Event
)


@admin_bp.route("/")
@login_required
def dashboard():

    # ==========================================================
    # DASHBOARD STATISTICS
    # ==========================================================

    stats = {
        "news": News.query.count(),

        "published_news": (
            News.query
            .filter_by(status="published")
            .count()
        ),

        "draft_news": (
            News.query
            .filter_by(status="draft")
            .count()
        ),

        "gallery": Gallery.query.count(),

        "hero": HeroSlide.query.count(),

        "members": Member.query.count(),

        "messages": ContactMessage.query.count(),

        "pages": Page.query.count(),

        "events": Event.query.count(),

        "users": User.query.count(),
    }


    # ==========================================================
    # RECENT NEWS
    # ==========================================================

    recent_news = (
        News.query
        .order_by(News.created_at.desc())
        .limit(5)
        .all()
    )


    # ==========================================================
    # RECENT EVENTS
    # ==========================================================

    recent_events = (
        Event.query
        .order_by(Event.created_at.desc())
        .limit(5)
        .all()
    )


    # ==========================================================
    # RECENT MESSAGES
    # ==========================================================

    recent_messages = (
        ContactMessage.query
        .order_by(ContactMessage.created_at.desc())
        .limit(5)
        .all()
    )


    # ==========================================================
    # RECENT MEMBERS
    # ==========================================================

    recent_members = (
        Member.query
        .order_by(Member.created_at.desc())
        .limit(5)
        .all()
    )


    # ==========================================================
    # RECENT GALLERY
    # ==========================================================

    recent_gallery = (
        Gallery.query
        .order_by(Gallery.created_at.desc())
        .limit(5)
        .all()
    )


    # ==========================================================
    # RECENT HERO SLIDES
    # ==========================================================

    recent_slides = (
        HeroSlide.query
        .order_by(HeroSlide.display_order.asc())
        .limit(5)
        .all()
    )


    # ==========================================================
    # RENDER DASHBOARD
    # ==========================================================

    return render_template(
        "admin/dashboard.html",

        stats=stats,

        recent_news=recent_news,

        recent_events=recent_events,

        recent_messages=recent_messages,

        recent_members=recent_members,

        recent_gallery=recent_gallery,

        recent_slides=recent_slides
    )