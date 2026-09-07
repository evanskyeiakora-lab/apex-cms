from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from . import pages_bp

from .forms import (
    PageForm,
    DeletePageForm
)

from app.extensions import db

from app.models import Page

from app.utils.file_upload import (
    replace_image,
    delete_image
)

from app.utils.slug import (
    generate_unique_slug
)

from app.utils.permissions import (
    roles_required
)


# ==========================================
# Allowed Roles
# ==========================================

PAGE_ROLES = (
    "Super Admin",
    "Administrator",
    "Editor"
)


# ==========================================
# Pages List
# ==========================================

@pages_bp.route("/")
@roles_required(*PAGE_ROLES)
def index():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    search = request.args.get(
        "search",
        ""
    ).strip()

    # --------------------------------------
    # Delete form
    # --------------------------------------

    delete_form = DeletePageForm()

    # --------------------------------------
    # Base query
    # --------------------------------------

    query = Page.query

    # --------------------------------------
    # Search
    # --------------------------------------

    if search:

        query = query.filter(
            Page.title.ilike(
                f"%{search}%"
            )
        )

    # --------------------------------------
    # Pagination
    # --------------------------------------

    pages = (
        query
        .order_by(
            Page.created_at.desc()
        )
        .paginate(
            page=page,
            per_page=10,
            error_out=False
        )
    )

    # --------------------------------------
    # Render
    # --------------------------------------

    return render_template(
        "admin/pages/index.html",
        pages=pages,
        search=search,
        delete_form=delete_form
    )


# ==========================================
# Create Page
# ==========================================

@pages_bp.route(
    "/create",
    methods=["GET", "POST"]
)
@roles_required(*PAGE_ROLES)
def create():

    form = PageForm()

    # --------------------------------------
    # Validate form
    # --------------------------------------

    if form.validate_on_submit():

        # ----------------------------------
        # Special page role protection
        # ----------------------------------

        if form.page_role.data != "normal":

            existing = Page.query.filter_by(
                page_role=form.page_role.data
            ).first()

            if existing:

                flash(
                    f"The role '{form.page_role.data}' "
                    f"is already assigned to "
                    f"'{existing.title}'.",
                    "danger"
                )

                return render_template(
                    "admin/pages/create.html",
                    form=form
                )

        # ----------------------------------
        # Featured image
        # ----------------------------------

        filename = None

        if form.featured_image.data:

            from app.utils.file_upload import (
                save_image
            )

            filename = save_image(
                form.featured_image.data,
                "pages"
            )

        # ----------------------------------
        # Slug
        # ----------------------------------

        slug = (
            form.slug.data.strip()
            if form.slug.data
            else ""
        )

        if not slug:

            slug = generate_unique_slug(
                Page,
                form.title.data,
                None
            )

        # ----------------------------------
        # Create page
        # ----------------------------------

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

        # ----------------------------------
        # Save
        # ----------------------------------

        db.session.add(
            page
        )

        db.session.commit()

        # ----------------------------------
        # Success message
        # ----------------------------------

        flash(
            "Page created successfully.",
            "success"
        )

        return redirect(
            url_for("pages.index")
        )

    # --------------------------------------
    # Render create form
    # --------------------------------------

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
@roles_required(*PAGE_ROLES)
def edit(id):

    page = Page.query.get_or_404(
        id
    )

    form = PageForm(
        obj=page
    )

    # --------------------------------------
    # Validate form
    # --------------------------------------

    if form.validate_on_submit():

        # ----------------------------------
        # Special page role protection
        # ----------------------------------

        if form.page_role.data != "normal":

            existing = (
                Page.query
                .filter(
                    Page.page_role == form.page_role.data,
                    Page.id != page.id
                )
                .first()
            )

            if existing:

                flash(
                    f"The role '{form.page_role.data}' "
                    f"is already assigned to "
                    f"'{existing.title}'.",
                    "danger"
                )

                return render_template(
                    "admin/pages/edit.html",
                    form=form,
                    page=page
                )

        # ----------------------------------
        # Basic information
        # ----------------------------------

        page.title = (
            form.title.data
        )

        # ----------------------------------
        # Slug
        # ----------------------------------

        submitted_slug = (
            form.slug.data.strip()
            if form.slug.data
            else ""
        )

        if submitted_slug:

            page.slug = generate_unique_slug(
                Page,
                submitted_slug,
                page.id
            )

        else:

            page.slug = generate_unique_slug(
                Page,
                form.title.data,
                page.id
            )

        # ----------------------------------
        # Page role
        # ----------------------------------

        page.page_role = (
            form.page_role.data
        )

        # ----------------------------------
        # Content
        # ----------------------------------

        page.content = (
            form.content.data
        )

        # ----------------------------------
        # SEO
        # ----------------------------------

        page.meta_title = (
            form.meta_title.data
        )

        page.meta_description = (
            form.meta_description.data
        )

        # ----------------------------------
        # Published status
        # ----------------------------------

        page.is_published = (
            form.is_published.data
        )

        # ----------------------------------
        # Featured image
        # ----------------------------------

        page.featured_image = replace_image(
            page.featured_image,
            form.featured_image.data,
            "pages"
        )

        # ----------------------------------
        # Save changes
        # ----------------------------------

        db.session.commit()

        # ----------------------------------
        # Success message
        # ----------------------------------

        flash(
            "Page updated successfully.",
            "success"
        )

        return redirect(
            url_for("pages.index")
        )

    # --------------------------------------
    # Render edit form
    # --------------------------------------

    return render_template(
        "admin/pages/edit.html",
        form=form,
        page=page
    )


# ==========================================
# Delete Page
# ==========================================

@pages_bp.route(
    "/delete/<int:id>",
    methods=["POST"]
)
@roles_required(*PAGE_ROLES)
def delete(id):

    # --------------------------------------
    # Validate CSRF
    # --------------------------------------

    form = DeletePageForm()

    if not form.validate_on_submit():

        flash(
            "Invalid delete request.",
            "danger"
        )

        return redirect(
            url_for("pages.index")
        )

    # --------------------------------------
    # Find page
    # --------------------------------------

    page = Page.query.get_or_404(
        id
    )

    # --------------------------------------
    # Delete featured image
    # --------------------------------------

    if page.featured_image:

        delete_image(
            page.featured_image,
            "pages"
        )

    # --------------------------------------
    # Delete database record
    # --------------------------------------

    db.session.delete(
        page
    )

    db.session.commit()

    # --------------------------------------
    # Success message
    # --------------------------------------

    flash(
        "Page deleted successfully.",
        "success"
    )

    return redirect(
        url_for("pages.index")
    )