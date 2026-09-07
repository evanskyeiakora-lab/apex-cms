from datetime import datetime

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import login_required

from . import news_bp
from .forms import NewsForm

from app.extensions import db
from app.models import News

from app.utils.file_upload import (
    replace_image,
    delete_image
)

from app.utils.permissions import roles_required

from app.utils.constants import NEWS_FOLDER


# ==========================================================
# ALLOWED ROLES
# ==========================================================

NEWS_ROLES = (
    "Super Admin",
    "Administrator",
    "Editor",
    "Author"
)


# ==========================================================
# NEWS LIST
# ==========================================================

@news_bp.route("/")
@login_required
@roles_required(*NEWS_ROLES)
def index():

    search = request.args.get(
        "search",
        ""
    ).strip()

    page = request.args.get(
        "page",
        1,
        type=int
    )

    query = News.query

    # ------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------

    if search:

        query = query.filter(
            News.title.ilike(
                f"%{search}%"
            )
        )

    # ------------------------------------------------------
    # PAGINATION
    # ------------------------------------------------------

    news = (
        query
        .order_by(
            News.created_at.desc()
        )
        .paginate(
            page=page,
            per_page=10,
            error_out=False
        )
    )

    return render_template(
        "admin/news/index.html",
        news=news,
        search=search
    )


# ==========================================================
# CREATE NEWS
# ==========================================================

@news_bp.route(
    "/create",
    methods=["GET", "POST"]
)
@login_required
@roles_required(*NEWS_ROLES)
def create():

    form = NewsForm()

    if form.validate_on_submit():

        # --------------------------------------------------
        # CREATE NEWS ARTICLE
        # --------------------------------------------------

        article = News(
            title=form.title.data.strip(),
            content=form.content.data,
            is_published=form.is_published.data
        )

        # --------------------------------------------------
        # GENERATE SLUG
        # --------------------------------------------------

        article.generate_slug()

        # --------------------------------------------------
        # SET PUBLISHED DATE
        # --------------------------------------------------

        if article.is_published:

            article.published_at = datetime.utcnow()

        else:

            article.published_at = None

        # --------------------------------------------------
        # SAVE FEATURED IMAGE
        # --------------------------------------------------

        if (
            form.featured_image.data
            and hasattr(
                form.featured_image.data,
                "filename"
            )
            and form.featured_image.data.filename
        ):

            article.featured_image = replace_image(
                None,
                form.featured_image.data,
                NEWS_FOLDER
            )

        try:

            db.session.add(article)

            db.session.commit()

            flash(
                "News created successfully.",
                "success"
            )

            return redirect(
                url_for("news.index")
            )

        except Exception as error:

            db.session.rollback()

            flash(
                "An error occurred while creating the news article.",
                "danger"
            )

            print(
                f"News creation error: {error}"
            )

    return render_template(
        "admin/news/create.html",
        form=form
    )


# ==========================================================
# EDIT NEWS
# ==========================================================

@news_bp.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
@roles_required(*NEWS_ROLES)
def edit(id):

    article = News.query.get_or_404(
        id
    )

    form = NewsForm(
        obj=article
    )

    if form.validate_on_submit():

        # --------------------------------------------------
        # UPDATE BASIC INFORMATION
        # --------------------------------------------------

        article.title = (
            form.title.data.strip()
        )

        article.content = (
            form.content.data
        )

        # --------------------------------------------------
        # UPDATE PUBLISH STATUS
        # --------------------------------------------------

        article.is_published = (
            form.is_published.data
        )

        # --------------------------------------------------
        # REGENERATE SLUG
        # --------------------------------------------------

        article.generate_slug()

        # --------------------------------------------------
        # HANDLE PUBLISHED DATE
        # --------------------------------------------------

        if article.is_published:

            if article.published_at is None:

                article.published_at = (
                    datetime.utcnow()
                )

        else:

            article.published_at = None

        # --------------------------------------------------
        # REPLACE FEATURED IMAGE
        # --------------------------------------------------

        if (
            form.featured_image.data
            and hasattr(
                form.featured_image.data,
                "filename"
            )
            and form.featured_image.data.filename
        ):

            article.featured_image = replace_image(
                article.featured_image,
                form.featured_image.data,
                NEWS_FOLDER
            )

        try:

            db.session.commit()

            flash(
                "News updated successfully.",
                "success"
            )

            return redirect(
                url_for("news.index")
            )

        except Exception as error:

            db.session.rollback()

            flash(
                "An error occurred while updating the news article.",
                "danger"
            )

            print(
                f"News update error: {error}"
            )

    # ------------------------------------------------------
    # POPULATE FORM ON GET REQUEST
    # ------------------------------------------------------

    if request.method == "GET":

        form.is_published.data = (
            article.is_published
        )

    return render_template(
        "admin/news/edit.html",
        form=form,
        article=article
    )


# ==========================================================
# DELETE NEWS
# ==========================================================

@news_bp.route(
    "/delete/<int:id>",
    methods=["POST"]
)
@login_required
@roles_required(*NEWS_ROLES)
def delete(id):

    article = News.query.get_or_404(
        id
    )

    try:

        # --------------------------------------------------
        # DELETE FEATURED IMAGE
        # --------------------------------------------------

        if article.featured_image:

            delete_image(
                article.featured_image,
                NEWS_FOLDER
            )

        # --------------------------------------------------
        # DELETE DATABASE RECORD
        # --------------------------------------------------

        db.session.delete(
            article
        )

        db.session.commit()

        flash(
            "News deleted successfully.",
            "success"
        )

    except Exception as error:

        db.session.rollback()

        flash(
            "An error occurred while deleting the news article.",
            "danger"
        )

        print(
            f"News deletion error: {error}"
        )

    return redirect(
        url_for("news.index")
    )