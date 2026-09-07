from flask import (
    render_template,
    redirect,
    url_for,
    request,
    current_app,
    flash
)

from flask_login import login_required

from . import hero_bp
from .forms import HeroForm

from app.models import HeroSlide

from app.utils import (
    replace_image,
    delete_image,
    save,
    commit,
    delete,
    flash_success
)

from app.utils.constants import HERO_FOLDER

from app.utils.permissions import roles_required


# ==========================================================
# ALLOWED ROLES
# ==========================================================

HERO_ROLES = (
    "Super Admin",
    "Administrator",
    "Editor"
)


# ==========================================================
# HERO SLIDER LIST
# ==========================================================

@hero_bp.route("/")
@login_required
@roles_required(*HERO_ROLES)
def index():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    slides = (
        HeroSlide.query
        .order_by(
            HeroSlide.display_order.asc(),
            HeroSlide.created_at.desc()
        )
        .paginate(
            page=page,
            per_page=10,
            error_out=False
        )
    )

    return render_template(
        "admin/hero/index.html",
        slides=slides
    )


# ==========================================================
# CREATE HERO SLIDE
# ==========================================================

@hero_bp.route(
    "/create",
    methods=["GET", "POST"]
)
@login_required
@roles_required(*HERO_ROLES)
def create():

    form = HeroForm()

    # ------------------------------------------------------
    # PROCESS FORM
    # ------------------------------------------------------

    if form.validate_on_submit():

        image_file = form.image.data

        # --------------------------------------------------
        # IMAGE IS REQUIRED WHEN CREATING
        # --------------------------------------------------

        if not image_file or not getattr(
            image_file,
            "filename",
            ""
        ):

            form.image.errors.append(
                "Please upload a hero image."
            )

            return render_template(
                "admin/hero/create.html",
                form=form
            )

        try:

            # ----------------------------------------------
            # CREATE SLIDE
            # ----------------------------------------------

            slide = HeroSlide(
                title=form.title.data.strip(),
                subtitle=form.subtitle.data,
                button_text=form.button_text.data,
                button_url=form.button_url.data,
                display_order=form.display_order.data or 1,
                is_active=form.is_active.data
            )

            # ----------------------------------------------
            # SAVE IMAGE
            # ----------------------------------------------

            slide.image = replace_image(
                None,
                image_file,
                HERO_FOLDER
            )

            # ----------------------------------------------
            # VERIFY IMAGE
            # ----------------------------------------------

            if not slide.image:

                form.image.errors.append(
                    "The hero image could not be saved."
                )

                return render_template(
                    "admin/hero/create.html",
                    form=form
                )

            # ----------------------------------------------
            # SAVE DATABASE RECORD
            # ----------------------------------------------

            save(slide)

            # ----------------------------------------------
            # SUCCESS
            # ----------------------------------------------

            flash_success(
                "Hero slide created successfully."
            )

            return redirect(
                url_for("hero.index")
            )

        except Exception as error:

            from app.extensions import db

            db.session.rollback()

            current_app.logger.exception(
                "Hero slide creation error: %s",
                error
            )

            # ----------------------------------------------
            # CLEAN UP IMAGE IF DATABASE SAVE FAILED
            # ----------------------------------------------

            try:

                if (
                    "slide" in locals()
                    and slide.image
                ):

                    delete_image(
                        slide.image,
                        HERO_FOLDER
                    )

            except Exception as image_error:

                current_app.logger.exception(
                    "Hero image cleanup error: %s",
                    image_error
                )

            form.image.errors.append(
                "An error occurred while creating the hero slide."
            )

    # ------------------------------------------------------
    # LOG VALIDATION ERRORS
    # ------------------------------------------------------

    if request.method == "POST" and form.errors:

        current_app.logger.warning(
            "Hero create validation errors: %s",
            form.errors
        )

    return render_template(
        "admin/hero/create.html",
        form=form
    )


# ==========================================================
# EDIT HERO SLIDE
# ==========================================================

@hero_bp.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
@roles_required(*HERO_ROLES)
def edit(id):

    slide = HeroSlide.query.get_or_404(
        id
    )

    form = HeroForm(
        obj=slide
    )

    # ------------------------------------------------------
    # PROCESS FORM
    # ------------------------------------------------------

    if form.validate_on_submit():

        old_image = slide.image

        try:

            # ----------------------------------------------
            # BASIC INFORMATION
            # ----------------------------------------------

            slide.title = (
                form.title.data.strip()
            )

            slide.subtitle = (
                form.subtitle.data
            )

            slide.button_text = (
                form.button_text.data
            )

            slide.button_url = (
                form.button_url.data
            )

            slide.display_order = (
                form.display_order.data or 1
            )

            slide.is_active = (
                form.is_active.data
            )

            # ----------------------------------------------
            # CHECK FOR NEW IMAGE
            # ----------------------------------------------

            image_file = form.image.data

            if (
                image_file
                and getattr(
                    image_file,
                    "filename",
                    ""
                )
            ):

                new_image = replace_image(
                    old_image,
                    image_file,
                    HERO_FOLDER
                )

                if not new_image:

                    raise RuntimeError(
                        "The new hero image could not be saved."
                    )

                slide.image = new_image

            # ----------------------------------------------
            # SAVE CHANGES
            # ----------------------------------------------

            commit()

            # ----------------------------------------------
            # SUCCESS
            # ----------------------------------------------

            flash_success(
                "Hero slide updated successfully."
            )

            return redirect(
                url_for("hero.index")
            )

        except Exception as error:

            from app.extensions import db

            db.session.rollback()

            current_app.logger.exception(
                "Hero slide update error for ID %s: %s",
                id,
                error
            )

            # Restore original image reference
            slide.image = old_image

            flash(
                "An error occurred while updating the hero slide.",
                "danger"
            )

    # ------------------------------------------------------
    # LOG VALIDATION ERRORS
    # ------------------------------------------------------

    if request.method == "POST" and form.errors:

        current_app.logger.warning(
            "Hero edit validation errors for ID %s: %s",
            id,
            form.errors
        )

    return render_template(
        "admin/hero/edit.html",
        form=form,
        slide=slide
    )


# ==========================================================
# DELETE HERO SLIDE
# ==========================================================

@hero_bp.route(
    "/delete/<int:id>",
    methods=["POST"]
)
@login_required
@roles_required(*HERO_ROLES)
def delete_slide(id):

    slide = HeroSlide.query.get_or_404(
        id
    )

    image = slide.image

    try:

        # --------------------------------------------------
        # DELETE DATABASE RECORD
        # --------------------------------------------------

        delete(slide)

        # --------------------------------------------------
        # DELETE IMAGE FROM STORAGE
        # --------------------------------------------------

        if image:

            delete_image(
                image,
                HERO_FOLDER
            )

        # --------------------------------------------------
        # SUCCESS
        # --------------------------------------------------

        flash_success(
            "Hero slide deleted successfully."
        )

    except Exception as error:

        from app.extensions import db

        db.session.rollback()

        current_app.logger.exception(
            "Hero slide deletion error for ID %s: %s",
            id,
            error
        )

        flash(
            "An error occurred while deleting the hero slide.",
            "danger"
        )

    return redirect(
        url_for("hero.index")
    )