from datetime import datetime

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import login_required

from . import events_bp
from .forms import EventForm

from app.extensions import db
from app.models import Event

from app.utils.file_upload import (
    replace_image,
    delete_image
)

from app.utils.permissions import roles_required

from app.utils.constants import EVENTS_FOLDER


# ==========================================================
# ALLOWED ROLES
# ==========================================================

EVENT_ROLES = (
    "Super Admin",
    "Administrator",
    "Editor",
    "Author"
)


# ==========================================================
# EVENTS LIST
# ==========================================================

@events_bp.route("/")
@login_required
@roles_required(*EVENT_ROLES)
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

    query = Event.query

    # ------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------

    if search:

        query = query.filter(
            Event.title.ilike(
                f"%{search}%"
            )
        )

    # ------------------------------------------------------
    # PAGINATION
    # ------------------------------------------------------

    events = (
        query
        .order_by(
            Event.start_date.asc(),
            Event.start_time.asc()
        )
        .paginate(
            page=page,
            per_page=10,
            error_out=False
        )
    )

    return render_template(
        "admin/events/index.html",
        events=events,
        search=search
    )


# ==========================================================
# CREATE EVENT
# ==========================================================

@events_bp.route(
    "/create",
    methods=["GET", "POST"]
)
@login_required
@roles_required(*EVENT_ROLES)
def create():

    form = EventForm()

    if form.validate_on_submit():

        # --------------------------------------------------
        # CREATE EVENT
        # --------------------------------------------------

        event = Event(
            title=form.title.data.strip(),
            description=form.description.data,
            venue=form.venue.data,
            organizer=form.organizer.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            registration_link=form.registration_link.data,
            is_featured=form.is_featured.data,
            is_published=form.is_published.data,
            display_order=form.display_order.data or 1
        )

        # --------------------------------------------------
        # GENERATE SLUG
        # --------------------------------------------------

        event.generate_slug()

        # --------------------------------------------------
        # PUBLISHED DATE
        # --------------------------------------------------

        if event.is_published:

            event.published_at = (
                datetime.utcnow()
            )

        else:

            event.published_at = None

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

            event.featured_image = replace_image(
                None,
                form.featured_image.data,
                EVENTS_FOLDER
            )

        try:

            db.session.add(event)

            db.session.commit()

            flash(
                "Event created successfully.",
                "success"
            )

            return redirect(
                url_for("events.index")
            )

        except Exception as error:

            db.session.rollback()

            flash(
                "An error occurred while creating the event.",
                "danger"
            )

            print(
                f"Event creation error: {error}"
            )

    return render_template(
        "admin/events/create.html",
        form=form
    )


# ==========================================================
# EDIT EVENT
# ==========================================================

@events_bp.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
@roles_required(*EVENT_ROLES)
def edit(id):

    event = Event.query.get_or_404(
        id
    )

    form = EventForm(
        obj=event
    )

    if form.validate_on_submit():

        # --------------------------------------------------
        # UPDATE BASIC INFORMATION
        # --------------------------------------------------

        event.title = (
            form.title.data.strip()
        )

        event.description = (
            form.description.data
        )

        event.venue = (
            form.venue.data
        )

        event.organizer = (
            form.organizer.data
        )

        event.start_date = (
            form.start_date.data
        )

        event.end_date = (
            form.end_date.data
        )

        event.start_time = (
            form.start_time.data
        )

        event.end_time = (
            form.end_time.data
        )

        event.registration_link = (
            form.registration_link.data
        )

        event.is_featured = (
            form.is_featured.data
        )

        event.is_published = (
            form.is_published.data
        )

        event.display_order = (
            form.display_order.data or 1
        )

        # --------------------------------------------------
        # REGENERATE SLUG
        # --------------------------------------------------

        event.generate_slug()

        # --------------------------------------------------
        # HANDLE PUBLISHED DATE
        # --------------------------------------------------

        if event.is_published:

            if event.published_at is None:

                event.published_at = (
                    datetime.utcnow()
                )

        else:

            event.published_at = None

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

            event.featured_image = replace_image(
                event.featured_image,
                form.featured_image.data,
                EVENTS_FOLDER
            )

        try:

            db.session.commit()

            flash(
                "Event updated successfully.",
                "success"
            )

            return redirect(
                url_for("events.index")
            )

        except Exception as error:

            db.session.rollback()

            flash(
                "An error occurred while updating the event.",
                "danger"
            )

            print(
                f"Event update error: {error}"
            )

    # ------------------------------------------------------
    # POPULATE FORM ON GET
    # ------------------------------------------------------

    if request.method == "GET":

        form.is_featured.data = (
            event.is_featured
        )

        form.is_published.data = (
            event.is_published
        )

    return render_template(
        "admin/events/edit.html",
        form=form,
        event=event
    )


# ==========================================================
# DELETE EVENT
# ==========================================================

@events_bp.route(
    "/delete/<int:id>",
    methods=["POST"]
)
@login_required
@roles_required(*EVENT_ROLES)
def delete(id):

    event = Event.query.get_or_404(
        id
    )

    try:

        # --------------------------------------------------
        # DELETE FEATURED IMAGE
        # --------------------------------------------------

        if event.featured_image:

            delete_image(
                event.featured_image,
                EVENTS_FOLDER
            )

        # --------------------------------------------------
        # DELETE DATABASE RECORD
        # --------------------------------------------------

        db.session.delete(
            event
        )

        db.session.commit()

        flash(
            "Event deleted successfully.",
            "success"
        )

    except Exception as error:

        db.session.rollback()

        flash(
            "An error occurred while deleting the event.",
            "danger"
        )

        print(
            f"Event deletion error: {error}"
        )

    return redirect(
        url_for("events.index")
    )