from flask import render_template
from flask_login import login_required

from . import admin_bp

from app.models import (
    News,
    Gallery,
    Member,
    ContactMessage,
    HeroSlide
)


@admin_bp.route("/")
@login_required
def dashboard():

    stats = {
        "news": News.query.count(),
        "published_news": News.query.filter_by(status="published").count(),
        "draft_news": News.query.filter_by(status="draft").count(),
        "gallery": Gallery.query.count(),
        "members": Member.query.count(),
        "messages": ContactMessage.query.count(),
    }

    recent_news = (
        News.query
        .order_by(News.created_at.desc())
        .limit(5)
        .all()
    )

    recent_messages = (
        ContactMessage.query
        .order_by(ContactMessage.created_at.desc())
        .limit(5)
        .all()
    )

    recent_slides = (
    HeroSlide.query
    .order_by(HeroSlide.created_at.desc())
    .limit(5)
    .all()
)


    return render_template(
    "admin/dashboard.html",
    stats=stats,
    recent_news=recent_news,
    recent_messages=recent_messages,
    recent_slides=recent_slides
)