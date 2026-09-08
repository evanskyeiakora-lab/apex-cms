# ==========================================================
# app/main/routes.py
# Apex Citizens of Ghana
# Public Website Routes
# ==========================================================

from datetime import date, time

from flask import (
    render_template,
    redirect,
    url_for,
    request
)

from . import main_bp

from app.models import (
    HeroSlide,
    Page,
    News,
    Event,
    Gallery,
    Member,
    Leader
)


# ==========================================================
# HOME
# ==========================================================

@main_bp.route("/")
def home():

    # ------------------------------------------------------
    # HERO SLIDES
    # ------------------------------------------------------

    slides = (
        HeroSlide.query
        .filter(
            HeroSlide.is_active.is_(True)
        )
        .order_by(
            HeroSlide.display_order.asc(),
            HeroSlide.id.asc()
        )
        .all()
    )

    # ------------------------------------------------------
    # ABOUT PAGE
    # ------------------------------------------------------

    about_page = (
        Page.query
        .filter(
            Page.page_role == "about-us",
            Page.is_published.is_(True)
        )
        .first()
    )

    # ------------------------------------------------------
    # VISION PAGE
    # ------------------------------------------------------

    vision_page = (
        Page.query
        .filter(
            Page.page_role == "vision",
            Page.is_published.is_(True)
        )
        .first()
    )

    # ------------------------------------------------------
    # MISSION PAGE
    # ------------------------------------------------------

    mission_page = (
        Page.query
        .filter(
            Page.page_role == "mission",
            Page.is_published.is_(True)
        )
        .first()
    )

    # ------------------------------------------------------
    # HISTORY PAGE
    # ------------------------------------------------------

    history_page = (
        Page.query
        .filter(
            Page.page_role == "history",
            Page.is_published.is_(True)
        )
        .first()
    )

    # ------------------------------------------------------
    # LATEST NEWS
    # ------------------------------------------------------

    latest_news = (
        News.query
        .filter(
            News.is_published.is_(True)
        )
        .order_by(
            News.published_at.desc(),
            News.id.desc()
        )
        .limit(3)
        .all()
    )

    # ------------------------------------------------------
    # UPCOMING EVENTS
    # ------------------------------------------------------

    upcoming_events = (
        Event.query
        .filter(
            Event.is_published.is_(True),
            Event.start_date >= date.today()
        )
        .order_by(
            Event.start_date.asc(),
            Event.start_time.asc(),
            Event.display_order.asc()
        )
        .limit(3)
        .all()
    )

    # ------------------------------------------------------
# HOMEPAGE GALLERY
# ------------------------------------------------------

    featured_gallery = (
        Gallery.query
        .filter(
        Gallery.is_published.is_(True)
    )
    .order_by(
        Gallery.display_order.asc(),
        Gallery.created_at.desc()
    )
    .limit(8)
    .all()
)

    # ------------------------------------------------------
    # LEADERSHIP
    # ------------------------------------------------------

    leaders = (
        Leader.query
        .filter(
            Leader.is_active.is_(True)
        )
        .order_by(
            Leader.display_order.asc(),
            Leader.name.asc()
        )
        .limit(8)
        .all()
    )

    # ------------------------------------------------------
    # WEBSITE STATISTICS
    # ------------------------------------------------------

    stats = {

        "members_count": (
            Member.query.count()
        ),

        "leaders_count": (
            Leader.query
            .filter(
                Leader.is_active.is_(True)
            )
            .count()
        ),

        "news_count": (
            News.query
            .filter(
                News.is_published.is_(True)
            )
            .count()
        ),

        "events_count": (
            Event.query
            .filter(
                Event.is_published.is_(True)
            )
            .count()
        ),

        "gallery_count": (
            Gallery.query
            .filter(
                Gallery.is_published.is_(True)
            )
            .count()
        )
    }

    # ------------------------------------------------------
    # RENDER HOMEPAGE
    # ------------------------------------------------------

    return render_template(
        "index.html",

        slides=slides,

        about_page=about_page,

        vision_page=vision_page,

        mission_page=mission_page,

        history_page=history_page,

        latest_news=latest_news,

        upcoming_events=upcoming_events,

        featured_gallery=featured_gallery,

        leaders=leaders,

        stats=stats
    )


# ==========================================================
# DYNAMIC WEBSITE PAGES
# ==========================================================

@main_bp.route(
    "/page/<slug>/"
)
def page(slug):

    website_page = (
        Page.query
        .filter(
            Page.slug == slug,
            Page.is_published.is_(True)
        )
        .first_or_404()
    )

    return render_template(
        "page.html",
        page=website_page
    )


# ==========================================================
# ABOUT
# ==========================================================

@main_bp.route(
    "/about/"
)
def about():

    about_page = (
        Page.query
        .filter(
            Page.page_role == "about-us",
            Page.is_published.is_(True)
        )
        .first()
    )

    # ------------------------------------------------------
    # ACTIVE LEADERS
    # ------------------------------------------------------

    leaders = (
        Leader.query
        .filter(
            Leader.is_active.is_(True)
        )
        .order_by(
            Leader.display_order.asc(),
            Leader.name.asc()
        )
        .all()
    )

    return render_template(
        "about.html",

        about_page=about_page,

        leaders=leaders
    )


# ==========================================================
# NEWS
# ==========================================================

@main_bp.route(
    "/news/"
)
def news():

    page_number = request.args.get(
        "page",
        1,
        type=int
    )

    news_items = (
        News.query
        .filter(
            News.is_published.is_(True)
        )
        .order_by(
            News.published_at.desc(),
            News.id.desc()
        )
        .paginate(
            page=page_number,
            per_page=9,
            error_out=False
        )
    )

    return render_template(
        "news/index.html",

        news=news_items
    )


# ==========================================================
# NEWS DETAIL
# ==========================================================

@main_bp.route(
    "/news/<slug>/"
)
def news_detail(slug):

    article = (
        News.query
        .filter(
            News.slug == slug,
            News.is_published.is_(True)
        )
        .first_or_404()
    )

    # ------------------------------------------------------
    # RELATED NEWS
    # ------------------------------------------------------

    related_news = (
        News.query
        .filter(
            News.is_published.is_(True),
            News.id != article.id
        )
        .order_by(
            News.published_at.desc(),
            News.id.desc()
        )
        .limit(5)
        .all()
    )

    return render_template(
        "news/detail.html",

        article=article,

        related_news=related_news
    )


# ==========================================================
# EVENTS
# ==========================================================

@main_bp.route(
    "/events/"
)
def events():

    # ------------------------------------------------------
    # TODAY
    # ------------------------------------------------------

    today = date.today()

    # ------------------------------------------------------
    # ALL PUBLISHED EVENTS
    # ------------------------------------------------------

    all_events = (
        Event.query
        .filter(
            Event.is_published.is_(True)
        )
        .order_by(
            Event.start_date.asc(),
            Event.start_time.asc(),
            Event.display_order.asc()
        )
        .all()
    )

    # ------------------------------------------------------
    # UPCOMING EVENTS
    # ------------------------------------------------------

    upcoming_events = [
        event
        for event in all_events
        if event.start_date
        and event.start_date >= today
    ]

    # ------------------------------------------------------
    # PAST EVENTS
    # ------------------------------------------------------

    past_events = [
        event
        for event in all_events
        if event.start_date
        and event.start_date < today
    ]

    # ------------------------------------------------------
    # SORT UPCOMING EVENTS
    # ------------------------------------------------------

    upcoming_events.sort(
        key=lambda event: (
            event.start_date,
            event.start_time or time.min,
            event.display_order or 1
        )
    )

    # ------------------------------------------------------
    # SORT PAST EVENTS
    # MOST RECENT FIRST
    # ------------------------------------------------------

    past_events.sort(
        key=lambda event: (
            event.start_date,
            event.start_time or time.min,
            event.display_order or 1
        ),
        reverse=True
    )

    # ------------------------------------------------------
    # RENDER EVENTS PAGE
    # ------------------------------------------------------

    return render_template(
        "events/index.html",

        events=all_events,

        upcoming_events=upcoming_events,

        past_events=past_events
    )


# ==========================================================
# EVENT DETAIL
# ==========================================================

@main_bp.route(
    "/events/<slug>/"
)
def event_detail(slug):

    event = (
        Event.query
        .filter(
            Event.slug == slug,
            Event.is_published.is_(True)
        )
        .first_or_404()
    )

    # ------------------------------------------------------
    # RELATED EVENTS
    # ------------------------------------------------------

    related_events = (
        Event.query
        .filter(
            Event.is_published.is_(True),
            Event.id != event.id
        )
        .order_by(
            Event.start_date.asc(),
            Event.start_time.asc(),
            Event.display_order.asc()
        )
        .limit(3)
        .all()
    )

    return render_template(
        "events/detail.html",

        event=event,

        related_events=related_events
    )


# ==========================================================
# GALLERY
# ==========================================================

@main_bp.route(
    "/gallery/"
)
def gallery():

    # ------------------------------------------------------
    # ACTIVE CATEGORY
    # ------------------------------------------------------

    active_category = (
        request.args
        .get(
            "category",
            ""
        )
        .strip()
    )

    # ------------------------------------------------------
    # BASE QUERY
    # ------------------------------------------------------

    query = (
        Gallery.query
        .filter(
            Gallery.is_published.is_(True)
        )
    )

    # ------------------------------------------------------
    # CATEGORY FILTER
    # ------------------------------------------------------

    if active_category:

        query = query.filter(
            Gallery.category == active_category
        )

    # ------------------------------------------------------
    # GALLERY ITEMS
    # ------------------------------------------------------

    gallery_items = (
        query
        .order_by(
            Gallery.is_featured.desc(),
            Gallery.display_order.asc(),
            Gallery.created_at.desc()
        )
        .all()
    )

    # ------------------------------------------------------
    # CATEGORIES
    # ------------------------------------------------------

    category_rows = (
        Gallery.query
        .with_entities(
            Gallery.category
        )
        .filter(
            Gallery.is_published.is_(True)
        )
        .distinct()
        .order_by(
            Gallery.category.asc()
        )
        .all()
    )

    categories = [
        category[0]
        for category in category_rows
        if category[0]
    ]

    # ------------------------------------------------------
    # RENDER GALLERY
    # ------------------------------------------------------

    return render_template(
        "gallery/index.html",

        galleries=gallery_items,

        gallery_items=gallery_items,

        categories=categories,

        active_category=active_category
    )


# ==========================================================
# GALLERY DETAIL
# ==========================================================

@main_bp.route(
    "/gallery/<slug>/"
)
def gallery_detail(slug):

    # ------------------------------------------------------
    # GET PUBLISHED GALLERY ITEM
    # ------------------------------------------------------

    gallery = (
        Gallery.query
        .filter(
            Gallery.slug == slug,
            Gallery.is_published.is_(True)
        )
        .first_or_404()
    )

    # ------------------------------------------------------
    # RELATED GALLERY ITEMS
    # ------------------------------------------------------

    related_images = (
        Gallery.query
        .filter(
            Gallery.is_published.is_(True),
            Gallery.category == gallery.category,
            Gallery.id != gallery.id
        )
        .order_by(
            Gallery.is_featured.desc(),
            Gallery.display_order.asc(),
            Gallery.created_at.desc()
        )
        .limit(6)
        .all()
    )

    # ------------------------------------------------------
    # RENDER GALLERY DETAIL
    # ------------------------------------------------------

    return render_template(
        "gallery/detail.html",

        gallery=gallery,

        related_images=related_images
    )


# ==========================================================
# LEADERSHIP
# ==========================================================

@main_bp.route(
    "/leadership/"
)
def leadership():

    # ------------------------------------------------------
    # ACTIVE LEADERS
    # ------------------------------------------------------

    leaders = (
        Leader.query
        .filter(
            Leader.is_active.is_(True)
        )
        .order_by(
            Leader.display_order.asc(),
            Leader.name.asc()
        )
        .all()
    )

    # ------------------------------------------------------
    # RENDER LEADERSHIP PAGE
    # ------------------------------------------------------

    return render_template(
        "leadership/index.html",

        leaders=leaders
    )


# ==========================================================
# MEMBERS
# ==========================================================

@main_bp.route(
    "/members/"
)
def members():

    page_number = request.args.get(
        "page",
        1,
        type=int
    )

    members = (
        Member.query
        .filter(
            Member.is_active.is_(True)
        )
        .order_by(
            Member.display_order.asc(),
            Member.full_name.asc()
        )
        .paginate(
            page=page_number,
            per_page=12,
            error_out=False
        )
    )

    return render_template(
        "members/index.html",

        members=members
    )


# ==========================================================
# JOIN US
# ==========================================================

@main_bp.route(
    "/join-us/"
)
def join_us():

    return redirect(
        url_for(
            "membership.apply"
        )
    )


# ==========================================================
# CONTACT
# ==========================================================

