from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from . import users_bp

from .forms import (
    UserForm,
    EditUserForm,
    ChangePasswordForm
)

from .services import UserService

from app.models import User

from app.utils.helpers import flash_success
from app.utils.permissions import admin_required


# ==========================================================
# Users List
# ==========================================================

@users_bp.route("/")
@login_required
@admin_required
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

    query = User.query

    if search:

        query = query.filter(
            User.first_name.ilike(f"%{search}%")
            |
            User.last_name.ilike(f"%{search}%")
            |
            User.username.ilike(f"%{search}%")
            |
            User.email.ilike(f"%{search}%")
        )

    users = (
        query
        .order_by(
            User.first_name.asc()
        )
        .paginate(
            page=page,
            per_page=10,
            error_out=False
        )
    )

    return render_template(
        "admin/users/index.html",
        users=users,
        search=search
    )


# ==========================================================
# Create User
# ==========================================================

@users_bp.route(
    "/create",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def create():

    form = UserForm()

    if form.validate_on_submit():

        try:

            UserService.create_user(form)

            flash_success(
                "User created successfully."
            )

            return redirect(
                url_for("users.index")
            )

        except ValueError as e:

            flash(
                str(e),
                "danger"
            )

    return render_template(
        "admin/users/create.html",
        form=form
    )


# ==========================================================
# Edit User
# ==========================================================

@users_bp.route(
    "/<int:id>/edit",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def edit(id):

    user = User.query.get_or_404(id)

    # Only a Super Admin can edit a Super Admin
    if (
        user.is_super_admin
        and not current_user.is_super_admin
    ):

        flash(
            "Only a Super Admin can edit a Super Admin account.",
            "danger"
        )

        return redirect(
            url_for("users.index")
        )

    form = EditUserForm(
        obj=user
    )

    if form.validate_on_submit():

        try:

            UserService.update_user(
                user,
                form
            )

            flash_success(
                "User updated successfully."
            )

            return redirect(
                url_for("users.index")
            )

        except ValueError as e:

            flash(
                str(e),
                "danger"
            )

    return render_template(
        "admin/users/edit.html",
        form=form,
        user=user
    )


# ==========================================================
# Delete User
# ==========================================================

@users_bp.route(
    "/<int:id>/delete",
    methods=["POST"]
)
@login_required
@admin_required
def delete(id):

    user = User.query.get_or_404(id)

    # Only a Super Admin can delete a Super Admin
    if (
        user.is_super_admin
        and not current_user.is_super_admin
    ):

        flash(
            "Only a Super Admin can delete a Super Admin account.",
            "danger"
        )

        return redirect(
            url_for("users.index")
        )

    try:

        UserService.delete_user(user)

        flash_success(
            "User deleted successfully."
        )

    except ValueError as e:

        flash(
            str(e),
            "danger"
        )

    return redirect(
        url_for("users.index")
    )


# ==========================================================
# My Profile
# ==========================================================

@users_bp.route(
    "/profile",
    methods=["GET", "POST"]
)
@login_required
def profile():

    form = EditUserForm(
        obj=current_user
    )

    if form.validate_on_submit():

        try:

            UserService.update_user(
                current_user,
                form,
                allow_role_change=False
            )

            flash_success(
                "Profile updated successfully."
            )

            return redirect(
                url_for("users.profile")
            )

        except ValueError as e:

            flash(
                str(e),
                "danger"
            )

    return render_template(
        "admin/users/profile.html",
        form=form
    )


# ==========================================================
# Change Password
# ==========================================================

@users_bp.route(
    "/change-password",
    methods=["GET", "POST"]
)
@login_required
def change_password():

    form = ChangePasswordForm()

    if form.validate_on_submit():

        if not current_user.check_password(
            form.current_password.data
        ):

            flash(
                "Current password is incorrect.",
                "danger"
            )

            return render_template(
                "admin/users/change_password.html",
                form=form
            )

        UserService.change_password(
            current_user,
            form.password.data
        )

        flash_success(
            "Password changed successfully."
        )

        return redirect(
            url_for("users.profile")
        )

    return render_template(
        "admin/users/change_password.html",
        form=form
    )


# ==========================================================
# User Details
# ==========================================================

@users_bp.route(
    "/<int:id>"
)
@login_required
@admin_required
def detail(id):

    user = User.query.get_or_404(id)

    return render_template(
        "admin/users/detail.html",
        user=user
    )