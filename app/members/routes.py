from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from . import members_bp

from .forms import (
    MemberForm,
    DeleteMemberForm
)

from app.extensions import db

from app.models import Member

from app.utils.file_upload import (
    save_image,
    delete_image
)

from app.utils.permissions import (
    roles_required
)


# ==========================================
# Allowed Roles
# ==========================================

MEMBER_ROLES = (
    "Super Admin",
    "Administrator",
    "Editor"
)


# ==========================================
# Members List
# ==========================================

@members_bp.route("/")
@roles_required(*MEMBER_ROLES)
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

    delete_form = DeleteMemberForm()

    # --------------------------------------
    # Base query
    # --------------------------------------

    query = Member.query

    # --------------------------------------
    # Search
    # --------------------------------------

    if search:

        query = query.filter(
            Member.full_name.ilike(
                f"%{search}%"
            )
        )

    # --------------------------------------
    # Pagination
    # --------------------------------------

    members = (
        query
        .order_by(
            Member.display_order.asc(),
            Member.full_name.asc()
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
        "admin/members/index.html",
        members=members,
        search=search,
        delete_form=delete_form
    )


# ==========================================
# Create Member
# ==========================================

@members_bp.route(
    "/create",
    methods=["GET", "POST"]
)
@roles_required(*MEMBER_ROLES)
def create():

    form = MemberForm()

    # --------------------------------------
    # Validate
    # --------------------------------------

    if form.validate_on_submit():

        filename = None

        # ----------------------------------
        # Member photo
        # ----------------------------------

        if form.photo.data:

            filename = save_image(
                form.photo.data,
                "members"
            )

        # ----------------------------------
        # Create member
        # ----------------------------------

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

        # ----------------------------------
        # Save
        # ----------------------------------

        db.session.add(
            member
        )

        db.session.commit()

        # ----------------------------------
        # Success
        # ----------------------------------

        flash(
            "Member created successfully.",
            "success"
        )

        return redirect(
            url_for("members.index")
        )

    # --------------------------------------
    # Render
    # --------------------------------------

    return render_template(
        "admin/members/create.html",
        form=form
    )


# ==========================================
# Edit Member
# ==========================================

@members_bp.route(
    "/edit/<int:id>",
    methods=["GET", "POST"]
)
@roles_required(*MEMBER_ROLES)
def edit(id):

    member = Member.query.get_or_404(
        id
    )

    form = MemberForm(
        obj=member
    )

    # --------------------------------------
    # Validate
    # --------------------------------------

    if form.validate_on_submit():

        # ----------------------------------
        # Basic information
        # ----------------------------------

        member.full_name = (
            form.full_name.data
        )

        member.position = (
            form.position.data
        )

        member.biography = (
            form.biography.data
        )

        # ----------------------------------
        # Contact information
        # ----------------------------------

        member.email = (
            form.email.data
        )

        member.phone = (
            form.phone.data
        )

        # ----------------------------------
        # Social media
        # ----------------------------------

        member.facebook = (
            form.facebook.data
        )

        member.linkedin = (
            form.linkedin.data
        )

        member.twitter = (
            form.twitter.data
        )

        # ----------------------------------
        # Display order
        # ----------------------------------

        member.display_order = (
            form.display_order.data
        )

        # ----------------------------------
        # Active status
        # ----------------------------------

        member.is_active = (
            form.is_active.data
        )

        # ----------------------------------
        # Replace photo
        # ----------------------------------

        if form.photo.data:

            old_photo = member.photo

            filename = save_image(
                form.photo.data,
                "members"
            )

            if filename:

                member.photo = filename

                # Delete old photo only after
                # new photo was successfully saved.

                if old_photo:

                    delete_image(
                        old_photo,
                        "members"
                    )

        # ----------------------------------
        # Save changes
        # ----------------------------------

        db.session.commit()

        # ----------------------------------
        # Success
        # ----------------------------------

        flash(
            "Member updated successfully.",
            "success"
        )

        return redirect(
            url_for("members.index")
        )

    # --------------------------------------
    # Render
    # --------------------------------------

    return render_template(
        "admin/members/edit.html",
        form=form,
        member=member
    )


# ==========================================
# Delete Member
# ==========================================

@members_bp.route(
    "/delete/<int:id>",
    methods=["POST"]
)
@roles_required(*MEMBER_ROLES)
def delete(id):

    # --------------------------------------
    # Validate CSRF
    # --------------------------------------

    form = DeleteMemberForm()

    if not form.validate_on_submit():

        flash(
            "Invalid delete request.",
            "danger"
        )

        return redirect(
            url_for("members.index")
        )

    # --------------------------------------
    # Find member
    # --------------------------------------

    member = Member.query.get_or_404(
        id
    )

    # --------------------------------------
    # Delete photo
    # --------------------------------------

    if member.photo:

        delete_image(
            member.photo,
            "members"
        )

    # --------------------------------------
    # Delete member
    # --------------------------------------

    db.session.delete(
        member
    )

    db.session.commit()

    # --------------------------------------
    # Success
    # --------------------------------------

    flash(
        "Member deleted successfully.",
        "success"
    )

    return redirect(
        url_for("members.index")
    )

