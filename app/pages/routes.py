from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import login_required

from . import pages_bp
from .forms import PageForm

from app.extensions import db
from app.models import Page
from app.utils.file_upload import save_image
from app.utils.slug import generate_unique_slug

# ==========================================
# Pages List
# ==========================================

@pages_bp.route("/")
@login_required
def index():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    search = request.args.get(
        "search",
        ""
    )

    query = Page.query

    if search:

        query = query.filter(
            Page.title.ilike(f"%{search}%")
        )

    pages = (
        query
        .order_by(Page.created_at.desc())
        .paginate(
            page=page,
            per_page=10,
            error_out=False
        )
    )

    return render_template(
        "admin/pages/index.html",
        pages=pages,
        search=search
    )


# ==========================================
# Create Page
# ==========================================

@pages_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():

    form = PageForm()

    if form.validate_on_submit():

        filename = None

        if form.featured_image.data:
            filename = save_image(
                form.featured_image.data,
                "pages"
            )

        # Auto-generate slug if left blank
        slug = form.slug.data.strip()

    if not slug:
        slug = generate_unique_slug(
        Page,
        form.title.data,
        page.id
    )

        # Ensure only one page can have a special role
        if form.page_role.data != "normal":

            existing = Page.query.filter_by(
                page_role=form.page_role.data
            ).first()

            if existing:

                flash(
                    f"The role '{form.page_role.data}' is already assigned to '{existing.title}'.",
                    "danger"
                )

                return render_template(
                    "admin/pages/create.html",
                    form=form
                )

        page = Page(
            title=form.title.data,
            slug=slug,
            page_role=form.page_role.data,
            content=form.content.data,
            featured_image=filename,
            meta_title=form.meta_title.data,
            meta_description=form.meta_description.data,
            is_published=form.is_published.data
        )

        db.session.add(page)
        db.session.commit()

        flash(
            "Page created successfully.",
            "success"
        )

        return redirect(
            url_for("pages.index")
        )

    return render_template(
        "admin/pages/create.html",
        form=form
    )

# ==========================================
# Edit Page
# ==========================================

@pages_bp.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit(id):

    page = Page.query.get_or_404(id)

    form = PageForm(
        obj=page
    )

    if form.validate_on_submit():

        page.title = form.title.data
        page.slug = form.slug.data
        page.content = form.content.data
        page.meta_title = form.meta_title.data
        page.meta_description = form.meta_description.data

        page.is_home_about = form.is_home_about.data
        page.is_published = form.is_published.data

        if form.featured_image.data:

            filename = save_image(
                form.featured_image.data,
                "pages"
            )

            if filename:
                page.featured_image = filename

        db.session.commit()

        flash(
            "Page updated successfully.",
            "success"
        )

        return redirect(
            url_for("pages.index")
        )

    return render_template(
        "admin/pages/edit.html",
        form=form,
        page=page
    )


# ==========================================
# Delete Page
# ==========================================

@pages_bp.route(
    "/delete/<int:id>"
)
@login_required
def delete(id):

    page = Page.query.get_or_404(id)

    db.session.delete(page)
    db.session.commit()

    flash(
        "Page deleted successfully.",
        "success"
    )

    return redirect(
        url_for("pages.index")
    )