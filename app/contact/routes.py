from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.extensions import db

from . import contact_bp

from .forms import ContactForm

from app.models import ContactMessage

# ============================================================
# PUBLIC CONTACT FORM
# ============================================================

@contact_bp.route(
    "/contact/",
    methods=["GET", "POST"]
)
def contact():

    form = ContactForm()

    if form.validate_on_submit():

        message = ContactMessage(
            name=form.name.data.strip(),

            email=form.email.data.strip(),

            phone=(
                form.phone.data.strip()
                if form.phone.data
                else None
            ),

            subject=form.subject.data.strip(),

            message=form.message.data.strip(),

            ip_address=request.remote_addr,

            user_agent=request.user_agent.string
        )

        try:

            db.session.add(message)

            db.session.commit()

            flash(
                "Thank you for contacting us. "
                "We have received your message.",
                "success"
            )

            return redirect(
                url_for("contact.contact")
            )

        except Exception as error:

            db.session.rollback()

            print(
                f"Contact message error: {error}"
            )

            flash(
                "Sorry, your message could not be sent. "
                "Please try again.",
                "danger"
            )

    return render_template(
        "contact/index.html",
        form=form
    )


# ============================================================
# ADMIN — CONTACT MESSAGES
# ============================================================

@contact_bp.route(
    "/admin/contact/"
)
def admin_index():

    search = request.args.get(
        "search",
        ""
    ).strip()

    page = request.args.get(
        "page",
        1,
        type=int
    )

    query = ContactMessage.query

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    if search:

        search_term = f"%{search}%"

        query = query.filter(
            ContactMessage.name.ilike(search_term)
            |
            ContactMessage.email.ilike(search_term)
            |
            ContactMessage.subject.ilike(search_term)
        )

    # --------------------------------------------------------
    # PAGINATION
    # --------------------------------------------------------

    messages = (
        query
        .order_by(
            ContactMessage.created_at.desc()
        )
        .paginate(
            page=page,
            per_page=20,
            error_out=False
        )
    )

    return render_template(
        "admin/contact/index.html",
        messages=messages,
        search=search
    )


# ============================================================
# ADMIN — VIEW MESSAGE
# ============================================================

@contact_bp.route(
    "/admin/contact/<int:id>"
)
def detail(id):

    message = ContactMessage.query.get_or_404(
        id
    )

    # --------------------------------------------------------
    # MARK AS READ
    # --------------------------------------------------------

    if not message.is_read:

        message.is_read = True

        db.session.commit()

    return render_template(
        "admin/contact/detail.html",
        message=message
    )


# ============================================================
# ADMIN — DELETE MESSAGE
# ============================================================

@contact_bp.route(
    "/admin/contact/<int:id>/delete",
    methods=["POST"]
)
def remove(id):

    message = ContactMessage.query.get_or_404(
        id
    )

    try:

        db.session.delete(message)

        db.session.commit()

        flash(
            "Message deleted successfully.",
            "success"
        )

    except Exception as error:

        db.session.rollback()

        print(
            f"Contact delete error: {error}"
        )

        flash(
            "Unable to delete message.",
            "danger"
        )

    return redirect(
        url_for("contact.admin_index")
    )