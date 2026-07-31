from flask import (
    render_template,
    redirect,
    url_for,
    request,
    current_app
)



from flask_login import login_required

from . import events_bp
from .forms import EventForm

from app.models import Event

from app.utils.database import (
    save,
    commit,
    delete
)

from app.utils.file_upload import (
    replace_image,
    delete_image
)

from app.utils.helpers import (
    flash_success
)

from app.utils.constants import EVENTS_FOLDER


# ==========================================
# Events List
# ==========================================
@events_bp.route("/")
@login_required
def index():

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    query = Event.query

    if search:
        query = query.filter(
            Event.title.ilike(f"%{search}%")
        )

    events = query.order_by(
        Event.start_date.desc()
    ).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    return render_template(
        "admin/events/index.html",
        events=events,
        search=search
    )


# ==========================================
# Create Event
# ==========================================
@events_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():

    form = EventForm()

    if form.validate_on_submit():

        event = Event(
            title=form.title.data,
            description=form.description.data,
            venue=form.venue.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            organizer=form.organizer.data,
            registration_link=form.registration_link.data,
            display_order=form.display_order.data,
            is_featured=form.is_featured.data,
            is_published=form.is_published.data
        )

        event.generate_slug()

        event.featured_image = replace_image(
            None,
            form.featured_image.data,
            EVENTS_FOLDER
        )

        save(event)

        flash_success(
            "Event created successfully."
        )

        return redirect(
            url_for("events.index")
        )

    if request.method == "POST":
        current_app.logger.warning(form.errors)

    return render_template(
        "admin/events/create.html",
        form=form
    )


# ==========================================
# Edit Event
# ==========================================
@events_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):

    event = Event.query.get_or_404(id)

    form = EventForm(obj=event)

    if form.validate_on_submit():

        event.title = form.title.data
        event.description = form.description.data
        event.venue = form.venue.data
        event.start_date = form.start_date.data
        event.end_date = form.end_date.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.organizer = form.organizer.data
        event.registration_link = form.registration_link.data
        event.display_order = form.display_order.data
        event.is_featured = form.is_featured.data
        event.is_published = form.is_published.data

        event.generate_slug()

        event.featured_image = replace_image(
            event.featured_image,
            form.featured_image.data,
            EVENTS_FOLDER
        )

        commit()

        flash_success(
            "Event updated successfully."
        )

        return redirect(
            url_for("events.index")
        )

    return render_template(
        "admin/events/edit.html",
        form=form,
        event=event
    )


# ==========================================
# Delete Event
# ==========================================
@events_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def remove(id):

    event = Event.query.get_or_404(id)

    delete_image(
        event.featured_image,
        EVENTS_FOLDER
    )

    delete(event)

    flash_success(
        "Event deleted successfully."
    )

    return redirect(
        url_for("events.index")
    )