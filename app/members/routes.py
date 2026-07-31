from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import login_required

from . import members_bp
from .forms import MemberForm

from app.extensions import db
from app.models import Member
from app.utils.file_upload import save_image


# ==========================================
# Members List
# ==========================================

@members_bp.route("/")
@login_required
def index():

    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")

    query = Member.query

    if search:
        query = query.filter(
            Member.full_name.ilike(f"%{search}%")
        )

    members = (
        query.order_by(
            Member.display_order.asc(),
            Member.full_name.asc()
        )
        .paginate(
            page=page,
            per_page=10,
            error_out=False
        )
    )

    return render_template(
        "admin/members/index.html",
        members=members,
        search=search
    )


# ==========================================
# Create Member
# ==========================================

@members_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():

    form = MemberForm()

    if form.validate_on_submit():

        filename = None

        if form.photo.data:
            filename = save_image(
                form.photo.data,
                "members"
            )

        member = Member(
            full_name=form.full_name.data,
            position=form.position.data,
            biography=form.biography.data,
            photo=filename,
            email=form.email.data,
            phone=form.phone.data,
            facebook=form.facebook.data,
            linkedin=form.linkedin.data,
            twitter=form.twitter.data,
            display_order=form.display_order.data,
            is_active=form.is_active.data
        )

        db.session.add(member)
        db.session.commit()

        flash(
            "Member created successfully.",
            "success"
        )

        return redirect(
            url_for("members.index")
        )

    return render_template(
        "admin/members/create.html",
        form=form
    )


# ==========================================
# Edit Member
# ==========================================

@members_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):

    member = Member.query.get_or_404(id)

    form = MemberForm(obj=member)

    if form.validate_on_submit():

        member.full_name = form.full_name.data
        member.position = form.position.data
        member.biography = form.biography.data
        member.email = form.email.data
        member.phone = form.phone.data
        member.facebook = form.facebook.data
        member.linkedin = form.linkedin.data
        member.twitter = form.twitter.data
        member.display_order = form.display_order.data
        member.is_active = form.is_active.data

        if form.photo.data:

            filename = save_image(
                form.photo.data,
                "members"
            )

            if filename:
                member.photo = filename

        db.session.commit()

        flash(
            "Member updated successfully.",
            "success"
        )

        return redirect(
            url_for("members.index")
        )

    return render_template(
        "admin/members/edit.html",
        form=form,
        member=member
    )


# ==========================================
# Delete Member
# ==========================================

@members_bp.route("/delete/<int:id>")
@login_required
def delete(id):

    member = Member.query.get_or_404(id)

    db.session.delete(member)
    db.session.commit()

    flash(
        "Member deleted successfully.",
        "success"
    )

    return redirect(
        url_for("members.index")
    )