from flask_login import current_user

from app.extensions import db
from app.models import User

from app.utils.file_upload import save_image
from app.utils.constants import USERS_FOLDER


class UserService:
    """
    Business logic for User management.
    """

    # =====================================================
    # Create User
    # =====================================================

    @staticmethod
    def create_user(form):

        # -------------------------------------------------
        # Super Admin protection
        # -------------------------------------------------

        if (
            form.role.data == "Super Admin"
            and not current_user.is_super_admin
        ):
            raise ValueError(
                "Only a Super Admin can create a Super Admin account."
            )

        # -------------------------------------------------
        # Check username
        # -------------------------------------------------

        username = form.username.data.strip()

        if User.query.filter_by(
            username=username
        ).first():

            raise ValueError(
                "Username already exists."
            )

        # -------------------------------------------------
        # Check email
        # -------------------------------------------------

        email = form.email.data.strip().lower()

        if User.query.filter_by(
            email=email
        ).first():

            raise ValueError(
                "Email address already exists."
            )

        # -------------------------------------------------
        # Save profile photo
        # -------------------------------------------------

        filename = None

        if form.photo.data:

            filename = save_image(
                form.photo.data,
                USERS_FOLDER
            )

        # -------------------------------------------------
        # Create user
        # -------------------------------------------------

        user = User(
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            username=username,
            email=email,
            phone=(
                form.phone.data.strip()
                if form.phone.data
                else None
            ),
            photo=filename,
            role=form.role.data,
            is_active=form.is_active.data
        )

        # -------------------------------------------------
        # Set password
        # -------------------------------------------------

        user.set_password(
            form.password.data
        )

        # -------------------------------------------------
        # Save
        # -------------------------------------------------

        db.session.add(user)
        db.session.commit()

        return user


    # =====================================================
    # Update User
    # =====================================================

    @staticmethod
    def update_user(
        user,
        form,
        allow_role_change=True
    ):

        # -------------------------------------------------
        # Check username
        # -------------------------------------------------

        username = form.username.data.strip()

        existing = User.query.filter_by(
            username=username
        ).first()

        if existing and existing.id != user.id:

            raise ValueError(
                "Username already exists."
            )

        # -------------------------------------------------
        # Check email
        # -------------------------------------------------

        email = form.email.data.strip().lower()

        existing = User.query.filter_by(
            email=email
        ).first()

        if existing and existing.id != user.id:

            raise ValueError(
                "Email address already exists."
            )

        # -------------------------------------------------
        # Super Admin role protection
        # -------------------------------------------------

        if allow_role_change:

            requested_role = form.role.data

            # ---------------------------------------------
            # Non-Super-Admin cannot assign Super Admin
            # ---------------------------------------------

            if (
                requested_role == "Super Admin"
                and not current_user.is_super_admin
            ):

                raise ValueError(
                    "Only a Super Admin can assign the Super Admin role."
                )

            # ---------------------------------------------
            # Prevent removing the last Super Admin
            # ---------------------------------------------

            if (
                user.is_super_admin
                and requested_role != "Super Admin"
            ):

                total_super_admins = (
                    User.query
                    .filter_by(role="Super Admin")
                    .count()
                )

                if total_super_admins <= 1:

                    raise ValueError(
                        "The last Super Admin cannot be demoted."
                    )

            # ---------------------------------------------
            # Prevent Super Admin from changing their own
            # Super Admin role
            # ---------------------------------------------

            if (
                user.id == current_user.id
                and user.is_super_admin
                and requested_role != "Super Admin"
            ):

                raise ValueError(
                    "You cannot remove the Super Admin role "
                    "from your own account."
                )

        # -------------------------------------------------
        # Update basic information
        # -------------------------------------------------

        user.first_name = (
            form.first_name.data.strip()
        )

        user.last_name = (
            form.last_name.data.strip()
        )

        user.username = username

        user.email = email

        user.phone = (
            form.phone.data.strip()
            if form.phone.data
            else None
        )

        # -------------------------------------------------
        # Update role
        # -------------------------------------------------

        if allow_role_change:

            user.role = form.role.data

        # -------------------------------------------------
        # Protect current Super Admin from self-deactivation
        # -------------------------------------------------

        if (
            user.id == current_user.id
            and user.is_super_admin
            and not form.is_active.data
        ):

            raise ValueError(
                "You cannot deactivate your own Super Admin account."
            )

        # -------------------------------------------------
        # Update active status
        # -------------------------------------------------

        user.is_active = form.is_active.data

        # -------------------------------------------------
        # Update profile photo
        # -------------------------------------------------

        if form.photo.data:

            filename = save_image(
                form.photo.data,
                USERS_FOLDER
            )

            if filename:
                user.photo = filename

        # -------------------------------------------------
        # Update password
        # -------------------------------------------------

        if form.password.data:

            user.set_password(
                form.password.data
            )

        # -------------------------------------------------
        # Save
        # -------------------------------------------------

        db.session.commit()

        return user


    # =====================================================
    # Delete User
    # =====================================================

    @staticmethod
    def delete_user(user):

        # -------------------------------------------------
        # Prevent deleting yourself
        # -------------------------------------------------

        if current_user.id == user.id:

            raise ValueError(
                "You cannot delete your own account."
            )

        # -------------------------------------------------
        # Protect Super Admin accounts
        # -------------------------------------------------

        if user.is_super_admin:

            total_super_admins = (
                User.query
                .filter_by(role="Super Admin")
                .count()
            )

            if total_super_admins <= 1:

                raise ValueError(
                    "The last Super Admin cannot be deleted."
                )

        # -------------------------------------------------
        # Delete
        # -------------------------------------------------

        db.session.delete(user)

        db.session.commit()


    # =====================================================
    # Change Password
    # =====================================================

    @staticmethod
    def change_password(
        user,
        password
    ):

        user.set_password(
            password
        )

        db.session.commit()

        return user


    # =====================================================
    # Activate User
    # =====================================================

    @staticmethod
    def activate(user):

        user.is_active = True

        db.session.commit()

        return user


    # =====================================================
    # Deactivate User
    # =====================================================

    @staticmethod
    def deactivate(user):

        # -------------------------------------------------
        # Prevent self-deactivation
        # -------------------------------------------------

        if current_user.id == user.id:

            raise ValueError(
                "You cannot deactivate your own account."
            )

        # -------------------------------------------------
        # Protect the last Super Admin
        # -------------------------------------------------

        if user.is_super_admin:

            total_super_admins = (
                User.query
                .filter_by(role="Super Admin")
                .count()
            )

            if total_super_admins <= 1:

                raise ValueError(
                    "The last Super Admin cannot be deactivated."
                )

        # -------------------------------------------------
        # Deactivate
        # -------------------------------------------------

        user.is_active = False

        db.session.commit()

        return user