from flask import (
    render_template,
    request,
    redirect,
    url_for
)

from flask_login import login_required

from . import contact_bp
from .forms import ContactForm

from app.models import ContactMessage

from app.utils.database import (
    save,
    commit,
    delete
)

from app.utils.helpers import flash_success


# ==========================================
# Public Contact Page
# ==========================================

@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():

    form = ContactForm()

    if form.validate_on_submit():

        message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=form.subject.data,
            message=form.message.data,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )

        save(message)

        flash_success(
            "Thank you for contacting us. We have received your message."
        )

        return redirect(url_for("contact.contact"))

    return render_template(
        "contact/index.html",
        form=form
    )


# ==========================================
# Admin Inbox
# ==========================================

@contact_bp.route("/admin/contact")
@login_required
def admin_index():

    search = request.args.get("search", "").strip()

    query = ContactMessage.query

    if search:
        query = query.filter(
            ContactMessage.name.ilike(f"%{search}%") |
            ContactMessage.email.ilike(f"%{search}%") |
            ContactMessage.subject.ilike(f"%{search}%")
        )

    page = request.args.get(
        "page",
        1,
        type=int
    )

    messages = query.order_by(
        ContactMessage.created_at.desc()
    ).paginate(
        page=page,
        per_page=20,
        error_out=False
    )

    return render_template(
        "admin/contact/index.html",
        messages=messages,
        search=search
    )


# ==========================================
# View Message
# ==========================================

@contact_bp.route("/admin/contact/<int:id>")
@login_required
def detail(id):

    message = ContactMessage.query.get_or_404(id)

    if not message.is_read:
        message.is_read = True
        commit()

    return render_template(
        "admin/contact/detail.html",
        message=message
    )


# ==========================================
# Delete Message
# ==========================================

@contact_bp.route(
    "/admin/contact/<int:id>/delete",
    methods=["POST"]
)
@login_required
def remove(id):

    message = ContactMessage.query.get_or_404(id)

    delete(message)

    flash_success(
        "Message deleted successfully."
    )

    return redirect(
        url_for("contact.admin_index")
    )