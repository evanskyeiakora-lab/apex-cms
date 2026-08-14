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
# Helper
# ==========================================================

def restrict_super_admin_role(form):
    """
    Hide the Super Admin role from non-Super-Admin users.

    The service layer also performs server-side protection,
    so removing the option from the form is not the only
    security measure.
    """

    if not current_user.is_super_admin:

        form.role.choices = [
            choice
            for choice in form.role.choices
            if choice[0] != "Super Admin"
        ]

    return form


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
            User.first_name.ilike(
                f"%{search}%"
            )
            |
            User.last_name.ilike(
                f"%{search}%"
            )
            |
            User.username.ilike(
                f"%{search}%"
            )
            |
            User.email.ilike(
                f"%{search}%"
            )
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

    # ------------------------------------------------------
    # Hide Super Admin from non-Super-Admins
    # ------------------------------------------------------

    restrict_super_admin_role(form)

    # ------------------------------------------------------
    # Process form
    # ------------------------------------------------------

    if form.validate_on_submit():

        # --------------------------------------------------
        # Server-side protection
        # --------------------------------------------------

        if (
            form.role.data == "Super Admin"
            and not current_user.is_super_admin
        ):

            flash(
                "Only a Super Admin can create a Super Admin account.",
                "danger"
            )

            return render_template(
                "admin/users/create.html",
                form=form
            )

        try:

            UserService.create_user(
                form
            )

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

    user = User.query.get_or_404(
        id
    )

    # ------------------------------------------------------
    # Protect Super Admin accounts
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # Create form
    # ------------------------------------------------------

    form = EditUserForm(
        obj=user
    )

    # ------------------------------------------------------
    # Hide Super Admin from non-Super-Admins
    # ------------------------------------------------------

    restrict_super_admin_role(form)

    # ------------------------------------------------------
    # Process form
    # ------------------------------------------------------

    if form.validate_on_submit():

        # --------------------------------------------------
        # Server-side role protection
        # --------------------------------------------------

        if (
            form.role.data == "Super Admin"
            and not current_user.is_super_admin
        ):

            flash(
                "Only a Super Admin can assign the Super Admin role.",
                "danger"
            )

            return render_template(
                "admin/users/edit.html",
                form=form,
                user=user
            )

        try:

            UserService.update_user(
                user,
                form,
                allow_role_change=True
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

    user = User.query.get_or_404(
        id
    )

    # ------------------------------------------------------
    # Protect Super Admin accounts
    # ------------------------------------------------------

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

        UserService.delete_user(
            user
        )

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

    # ------------------------------------------------------
    # A user cannot change their own role from profile
    # ------------------------------------------------------

    form.role.data = current_user.role

    # ------------------------------------------------------
    # Hide Super Admin option if necessary
    # ------------------------------------------------------

    restrict_super_admin_role(form)

    # ------------------------------------------------------
    # Process form
    # ------------------------------------------------------

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

        # --------------------------------------------------
        # Verify current password
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Change password
        # --------------------------------------------------

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

    user = User.query.get_or_404(
        id
    )

    return render_template(
        "admin/users/detail.html",
        user=user
    )