from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import login_required

from . import leaders_bp
from .forms import LeaderForm

from app.extensions import db
from app.models import Leader

from app.utils.file_upload import (
    replace_image,
    delete_image
)

from app.utils.permissions import roles_required
from app.utils.constants import LEADERS_FOLDER


# ==========================================================
# ALLOWED ROLES
# ==========================================================

LEADER_ROLES = (
    "Super Admin",
    "Administrator",
    "Editor"
)


# ==========================================================
# LEADERS LIST
# ==========================================================

@leaders_bp.route("/")
@login_required
@roles_required(*LEADER_ROLES)
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

    query = Leader.query

    # ------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------

    if search:

        query = query.filter(
            Leader.name.ilike(
                f"%{search}%"
            )
            |
            Leader.position.ilike(
                f"%{search}%"
            )
        )

    # ------------------------------------------------------
    # PAGINATION
    # ------------------------------------------------------

    leaders = (
        query
        .order_by(
            Leader.display_order.asc(),
            Leader.name.asc()
        )
        .paginate(
            page=page,
            per_page=10,
            error_out=False
        )
    )

    return render_template(
        "admin/leaders/index.html",
        leaders=leaders,
        search=search
    )


# ==========================================================
# CREATE LEADER
# ==========================================================

@leaders_bp.route(
    "/create",
    methods=["GET", "POST"]
)
@login_required
@roles_required(*LEADER_ROLES)
def create():

    form = LeaderForm()

    if form.validate_on_submit():

        leader = Leader(
            name=form.name.data.strip(),
            position=form.position.data.strip(),
            bio=form.bio.data,
            email=form.email.data,
            phone=form.phone.data,
            facebook=form.facebook.data,
            twitter=form.twitter.data,
            linkedin=form.linkedin.data,
            display_order=form.display_order.data or 1,
            is_active=form.is_active.data
        )

        # --------------------------------------------------
        # SAVE PHOTO
        # --------------------------------------------------

        if (
            form.photo.data
            and hasattr(
                form.photo.data,
                "filename"
            )
            and form.photo.data.filename
        ):

            leader.photo = replace_image(
                None,
                form.photo.data,
                LEADERS_FOLDER
            )

        try:

            db.session.add(
                leader
            )

            db.session.commit()

            flash(
                "Leader added successfully.",
                "success"
            )

            return redirect(
                url_for("leaders.index")
            )

        except Exception as error:

            db.session.rollback()

            flash(
                "An error occurred while adding the leader.",
                "danger"
            )

            print(
                f"Leader creation error: {error}"
            )

    return render_template(
        "admin/leaders/create.html",
        form=form
    )


# ==========================================================
# EDIT LEADER
# ==========================================================

@leaders_bp.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
@roles_required(*LEADER_ROLES)
def edit(id):

    leader = Leader.query.get_or_404(
        id
    )

    form = LeaderForm(
        obj=leader
    )

    if form.validate_on_submit():

        # --------------------------------------------------
        # BASIC INFORMATION
        # --------------------------------------------------

        leader.name = (
            form.name.data.strip()
        )

        leader.position = (
            form.position.data.strip()
        )

        leader.bio = (
            form.bio.data
        )

        leader.email = (
            form.email.data
        )

        leader.phone = (
            form.phone.data
        )

        leader.facebook = (
            form.facebook.data
        )

        leader.twitter = (
            form.twitter.data
        )

        leader.linkedin = (
            form.linkedin.data
        )

        leader.display_order = (
            form.display_order.data or 1
        )

        leader.is_active = (
            form.is_active.data
        )

        # --------------------------------------------------
        # REPLACE PHOTO
        # --------------------------------------------------

        if (
            form.photo.data
            and hasattr(
                form.photo.data,
                "filename"
            )
            and form.photo.data.filename
        ):

            leader.photo = replace_image(
                leader.photo,
                form.photo.data,
                LEADERS_FOLDER
            )

        try:

            db.session.commit()

            flash(
                "Leader updated successfully.",
                "success"
            )

            return redirect(
                url_for("leaders.index")
            )

        except Exception as error:

            db.session.rollback()

            flash(
                "An error occurred while updating the leader.",
                "danger"
            )

            print(
                f"Leader update error: {error}"
            )

    # ------------------------------------------------------
    # POPULATE CHECKBOXES ON GET
    # ------------------------------------------------------

    if request.method == "GET":

        form.is_active.data = (
            leader.is_active
        )

    return render_template(
        "admin/leaders/edit.html",
        form=form,
        leader=leader
    )


# ==========================================================
# DELETE LEADER
# ==========================================================

@leaders_bp.route(
    "/delete/<int:id>",
    methods=["POST"]
)
@login_required
@roles_required(*LEADER_ROLES)
def delete(id):

    leader = Leader.query.get_or_404(
        id
    )

    try:

        # --------------------------------------------------
        # DELETE PHOTO
        # --------------------------------------------------

        if leader.photo:

            delete_image(
                leader.photo,
                LEADERS_FOLDER
            )

        # --------------------------------------------------
        # DELETE DATABASE RECORD
        # --------------------------------------------------

        db.session.delete(
            leader
        )

        db.session.commit()

        flash(
            "Leader deleted successfully.",
            "success"
        )

    except Exception as error:

        db.session.rollback()

        flash(
            "An error occurred while deleting the leader.",
            "danger"
        )

        print(
            f"Leader deletion error: {error}"
        )

    return redirect(
        url_for("leaders.index")
    )