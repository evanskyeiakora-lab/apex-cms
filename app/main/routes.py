from flask import render_template

from . import main_bp
from app.models import News, HeroSlide


@main_bp.route("/")
def home():

    latest_news = (
        News.query
        .filter_by(status="published")
        .order_by(News.published_at.desc())
        .limit(3)
        .all()
    )

    slides = (
        HeroSlide.query
        .filter_by(is_active=True)
        .order_by(HeroSlide.display_order.asc())
        .all()
    )

    return render_template(
        "index.html",
        latest_news=latest_news,
        slides=slides
    )