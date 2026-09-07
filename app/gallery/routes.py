from datetime import datetime, timezone

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import login_required

from . import gallery_bp
from .forms import GalleryForm

from app.extensions import db
from app.models import Gallery

from app.utils.file_upload import (
    replace_image,
    delete_image
)

from app.utils.permissions import roles_required

from app.utils.constants import GALLERY_FOLDER


# ==========================================================
# ALLOWED ROLES
# ==========================================================

GALLERY_ROLES = (
    "Super Admin",
    "Administrator",
    "Editor",
    "Author"
)


# ==========================================================
# GALLERY LIST
# ==========================================================

@gallery_bp.route("/")
@login_required
@roles_required(*GALLERY_ROLES)
def index():

    # ------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------

    search = request.args.get(
        "search",
        ""
    ).strip()

    # ------------------------------------------------------
    # CATEGORY
    # ------------------------------------------------------

    category = request.args.get(
        "category",
        ""
    ).strip()

    # ------------------------------------------------------
    # PAGE
    # ------------------------------------------------------

    page = request.args.get(
        "page",
        1,
        type=int
    )

    # ------------------------------------------------------
    # BASE QUERY
    # ------------------------------------------------------

    query = Gallery.query

    # ------------------------------------------------------
    # SEARCH BY TITLE
    # ------------------------------------------------------

    if search:

        query = query.filter(
            Gallery.title.ilike(
                f"%{search}%"
            )
        )

    # ------------------------------------------------------
    # FILTER BY CATEGORY
    # ------------------------------------------------------

    if category:

        query = query.filter(
            Gallery.category == category
        )

    # ------------------------------------------------------
    # PAGINATION
    # ------------------------------------------------------

    galleries = (
        query
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

    # ------------------------------------------------------
    # AVAILABLE CATEGORIES
    # ------------------------------------------------------

    categories = [
        "General",
        "Church Service",
        "Conference",
        "Youth Ministry",
        "Women's Ministry",
        "Men's Ministry",
        "Children",
        "Outreach",
        "Community"
    ]

    # ------------------------------------------------------
    # RENDER
    # ------------------------------------------------------

    return render_template(
        "admin/gallery/index.html",
        galleries=galleries,
        search=search,
        category=category,
        categories=categories
    )


# ==========================================================
# CREATE GALLERY
# ==========================================================

@gallery_bp.route(
    "/create",
    methods=["GET", "POST"]
)
@login_required
@roles_required(*GALLERY_ROLES)
def create():

    form = GalleryForm()

    # ======================================================
    # FORM SUBMISSION
    # ======================================================

    if form.validate_on_submit():

        # --------------------------------------------------
        # IMAGE IS REQUIRED WHEN CREATING
        # --------------------------------------------------

        image_file = form.image.data

        if not image_file or not getattr(
            image_file,
            "filename",
            ""
        ):

            flash(
                "Please select a gallery image.",
                "danger"
            )

            return render_template(
                "admin/gallery/create.html",
                form=form
            )

        # --------------------------------------------------
        # CREATE GALLERY OBJECT
        # --------------------------------------------------

        gallery = Gallery(
            title=form.title.data.strip(),

            description=(
                form.description.data
                if form.description.data
                else None
            ),

            category=form.category.data,

            display_order=(
                form.display_order.data
                if form.display_order.data is not None
                else 0
            ),

            is_featured=form.is_featured.data,

            is_published=form.is_published.data
        )

        # --------------------------------------------------
        # GENERATE UNIQUE SLUG
        # --------------------------------------------------

        gallery.generate_slug()

        # --------------------------------------------------
        # PUBLISHED DATE
        # --------------------------------------------------

        if gallery.is_published:

            gallery.published_at = (
                datetime.now(timezone.utc)
            )

        else:

            gallery.published_at = None

        # --------------------------------------------------
        # SAVE IMAGE
        # --------------------------------------------------

        try:

            gallery.image = replace_image(
                None,
                image_file,
                GALLERY_FOLDER
            )

        except Exception as error:

            flash(
                "The gallery image could not be uploaded.",
                "danger"
            )

            print(
                f"Gallery image upload error: {error}"
            )

            return render_template(
                "admin/gallery/create.html",
                form=form
            )

        # --------------------------------------------------
        # SAVE DATABASE RECORD
        # --------------------------------------------------

        try:

            db.session.add(
                gallery
            )

            db.session.commit()

            flash(
                "Gallery image created successfully.",
                "success"
            )

            return redirect(
                url_for("gallery.index")
            )

        except Exception as error:

            db.session.rollback()

            # ----------------------------------------------
            # REMOVE UPLOADED IMAGE IF DATABASE SAVE FAILS
            # ----------------------------------------------

            if gallery.image:

                try:

                    delete_image(
                        gallery.image,
                        GALLERY_FOLDER
                    )

                except Exception as image_error:

                    print(
                        f"Gallery cleanup error: {image_error}"
                    )

            flash(
                "An error occurred while creating the gallery image.",
                "danger"
            )

            print(
                f"Gallery creation error: {error}"
            )

    # ======================================================
    # RENDER CREATE PAGE
    # ======================================================

    return render_template(
        "admin/gallery/create.html",
        form=form
    )


# ==========================================================
# EDIT GALLERY
# ==========================================================

@gallery_bp.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
@roles_required(*GALLERY_ROLES)
def edit(id):

    # ------------------------------------------------------
    # GET EXISTING GALLERY
    # ------------------------------------------------------

    gallery = Gallery.query.get_or_404(
        id
    )

    # ------------------------------------------------------
    # CREATE FORM
    # ------------------------------------------------------

    form = GalleryForm()

    # ======================================================
    # GET REQUEST
    # ======================================================

    if request.method == "GET":

        # --------------------------------------------------
        # POPULATE NORMAL FIELDS
        # --------------------------------------------------

        form.title.data = (
            gallery.title
        )

        form.description.data = (
            gallery.description
        )

        form.category.data = (
            gallery.category
        )

        form.display_order.data = (
            gallery.display_order
        )

        form.is_featured.data = (
            gallery.is_featured
        )

        form.is_published.data = (
            gallery.is_published
        )

    # ======================================================
    # POST REQUEST
    # ======================================================

    if form.validate_on_submit():

        # --------------------------------------------------
        # UPDATE TITLE
        # --------------------------------------------------

        gallery.title = (
            form.title.data.strip()
        )

        # --------------------------------------------------
        # UPDATE DESCRIPTION
        # --------------------------------------------------

        gallery.description = (
            form.description.data
            if form.description.data
            else None
        )

        # --------------------------------------------------
        # UPDATE CATEGORY
        # --------------------------------------------------

        gallery.category = (
            form.category.data
        )

        # --------------------------------------------------
        # UPDATE DISPLAY ORDER
        # --------------------------------------------------

        gallery.display_order = (
            form.display_order.data
            if form.display_order.data is not None
            else 0
        )

        # --------------------------------------------------
        # UPDATE FEATURED STATUS
        # --------------------------------------------------

        gallery.is_featured = (
            form.is_featured.data
        )

        # --------------------------------------------------
        # UPDATE PUBLISHED STATUS
        # --------------------------------------------------

        gallery.is_published = (
            form.is_published.data
        )

        # --------------------------------------------------
        # REGENERATE SLUG
        # --------------------------------------------------

        gallery.generate_slug()

        # --------------------------------------------------
        # HANDLE PUBLISHED DATE
        # --------------------------------------------------

        if gallery.is_published:

            if gallery.published_at is None:

                gallery.published_at = (
                    datetime.now(timezone.utc)
                )

        else:

            gallery.published_at = None

        # ==================================================
        # HANDLE IMAGE
        # ==================================================

        image_file = form.image.data

        # --------------------------------------------------
        # NO NEW IMAGE
        # --------------------------------------------------
        #
        # Keep the existing image.
        # --------------------------------------------------

        if not image_file or not getattr(
            image_file,
            "filename",
            ""
        ):

            pass

        # --------------------------------------------------
        # NEW IMAGE SELECTED
        # --------------------------------------------------

        else:

            try:

                gallery.image = replace_image(
                    gallery.image,
                    image_file,
                    GALLERY_FOLDER
                )

            except Exception as error:

                db.session.rollback()

                flash(
                    "The new gallery image could not be uploaded.",
                    "danger"
                )

                print(
                    f"Gallery image replacement error: {error}"
                )

                return render_template(
                    "admin/gallery/edit.html",
                    form=form,
                    gallery=gallery
                )

        # ==================================================
        # SAVE CHANGES
        # ==================================================

        try:

            db.session.commit()

            flash(
                "Gallery image updated successfully.",
                "success"
            )

            return redirect(
                url_for("gallery.index")
            )

        except Exception as error:

            db.session.rollback()

            flash(
                "An error occurred while updating the gallery image.",
                "danger"
            )

            print(
                f"Gallery update error: {error}"
            )

    # ======================================================
    # RENDER EDIT PAGE
    # ======================================================

    return render_template(
        "admin/gallery/edit.html",
        form=form,
        gallery=gallery
    )


# ==========================================================
# DELETE GALLERY
# ==========================================================

@gallery_bp.route(
    "/delete/<int:id>",
    methods=["POST"]
)
@login_required
@roles_required(*GALLERY_ROLES)
def delete(id):

    # ------------------------------------------------------
    # GET GALLERY
    # ------------------------------------------------------

    gallery = Gallery.query.get_or_404(
        id
    )

    try:

        # ==================================================
        # DELETE IMAGE
        # ==================================================

        if gallery.image:

            delete_image(
                gallery.image,
                GALLERY_FOLDER
            )

        # ==================================================
        # DELETE DATABASE RECORD
        # ==================================================

        db.session.delete(
            gallery
        )

        db.session.commit()

        flash(
            "Gallery image deleted successfully.",
            "success"
        )

    except Exception as error:

        db.session.rollback()

        flash(
            "An error occurred while deleting the gallery image.",
            "danger"
        )

        print(
            f"Gallery deletion error: {error}"
        )

    # ------------------------------------------------------
    # RETURN TO GALLERY
    # ------------------------------------------------------

    return redirect(
        url_for("gallery.index")
    )