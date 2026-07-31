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


# ======================================
# News List
# ======================================
@news_bp.route("/")
@login_required
def index():

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    query = News.query

    if search:
        query = query.filter(
            News.title.ilike(f"%{search}%")
        )

    news = query.order_by(
        News.created_at.desc()
    ).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    return render_template(
        "admin/news/index.html",
        news=news,
        search=search
    )


# ======================================
# Create News
# ======================================
@news_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():

    form = NewsForm()

    if form.validate_on_submit():

        article = News(
            title=form.title.data,
            content=form.content.data,
            status=form.status.data
        )

        article.generate_slug()

        if article.status == "published":
            article.published_at = datetime.utcnow()

        article.featured_image = replace_image(
            None,
            form.featured_image.data,
            "news"
        )

        db.session.add(article)
        db.session.commit()

        flash(
            "News created successfully.",
            "success"
        )

        return redirect(
            url_for("news.index")
        )

    return render_template(
        "admin/news/create.html",
        form=form
    )


# ======================================
# Edit News
# ======================================
@news_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):

    article = News.query.get_or_404(id)

    form = NewsForm(obj=article)

    if form.validate_on_submit():

        article.title = form.title.data
        article.content = form.content.data
        article.status = form.status.data

        article.generate_slug()

        if (
            article.status == "published"
            and article.published_at is None
        ):
            article.published_at = datetime.utcnow()

        article.featured_image = replace_image(
            article.featured_image,
            form.featured_image.data,
            "news"
        )

        db.session.commit()

        flash(
            "News updated successfully.",
            "success"
        )

        return redirect(
            url_for("news.index")
        )

    return render_template(
        "admin/news/edit.html",
        form=form,
        article=article
    )


# ======================================
# Delete News
# ======================================
@news_bp.route("/delete/<int:id>")
@login_required
def delete(id):

    article = News.query.get_or_404(id)

    delete_image(
        article.featured_image,
        "news"
    )

    db.session.delete(article)
    db.session.commit()

    flash(
        "News deleted successfully.",
        "success"
    )

    return redirect(
        url_for("news.index")
    )