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

        # Administrators cannot create Super Admin accounts
        if (
            not current_user.is_super_admin
            and form.role.data == "Super Admin"
        ):
            raise ValueError(
                "Only a Super Admin can create a Super Admin account."
            )

        # Check username
        if User.query.filter_by(
            username=form.username.data.strip()
        ).first():

            raise ValueError(
                "Username already exists."
            )

        # Check email
        if User.query.filter_by(
            email=form.email.data.strip().lower()
        ).first():

            raise ValueError(
                "Email address already exists."
            )

        filename = None

        if form.photo.data:

            filename = save_image(
                form.photo.data,
                USERS_FOLDER
            )

        user = User(
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            phone=(
                form.phone.data.strip()
                if form.phone.data
                else None
            ),
            photo=filename,
            role=form.role.data,
            is_active=form.is_active.data
        )

        user.set_password(
            form.password.data
        )

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
        # Protect Super Admin
        # -------------------------------------------------

        if (
            user.is_super_admin
            and not current_user.is_super_admin
        ):

            raise ValueError(
                "Only a Super Admin can modify a Super Admin account."
            )


        # -------------------------------------------------
        # Check username
        # -------------------------------------------------

        existing = User.query.filter_by(
            username=form.username.data.strip()
        ).first()

        if existing and existing.id != user.id:

            raise ValueError(
                "Username already exists."
            )


        # -------------------------------------------------
        # Check email
        # -------------------------------------------------

        existing = User.query.filter_by(
            email=form.email.data.strip().lower()
        ).first()

        if existing and existing.id != user.id:

            raise ValueError(
                "Email address already exists."
            )


        # -------------------------------------------------
        # Basic information
        # -------------------------------------------------

        user.first_name = (
            form.first_name.data.strip()
        )

        user.last_name = (
            form.last_name.data.strip()
        )

        user.username = (
            form.username.data.strip()
        )

        user.email = (
            form.email.data.strip().lower()
        )

        user.phone = (
            form.phone.data.strip()
            if form.phone.data
            else None
        )


        # -------------------------------------------------
        # Role
        # -------------------------------------------------

        if allow_role_change:

            if (
                not current_user.is_super_admin
                and form.role.data == "Super Admin"
            ):

                raise ValueError(
                    "Only a Super Admin can assign the Super Admin role."
                )

            user.role = form.role.data


        # -------------------------------------------------
        # Active status
        # -------------------------------------------------

        if (
            user.is_super_admin
            and not current_user.is_super_admin
        ):

            # Administrator cannot deactivate
            # a Super Admin.
            user.is_active = True

        else:

            user.is_active = (
                form.is_active.data
            )


        # -------------------------------------------------
        # Photo
        # -------------------------------------------------

        if form.photo.data:

            filename = save_image(
                form.photo.data,
                USERS_FOLDER
            )

            user.photo = filename


        # -------------------------------------------------
        # Password
        # -------------------------------------------------

        if form.password.data:

            user.set_password(
                form.password.data
            )


        db.session.commit()

        return user


    # =====================================================
    # Delete User
    # =====================================================

    @staticmethod
    def delete_user(user):

        # Prevent deleting yourself
        if current_user.id == user.id:

            raise ValueError(
                "You cannot delete your own account."
            )


        # Only Super Admin can delete another Super Admin
        if (
            user.is_super_admin
            and not current_user.is_super_admin
        ):

            raise ValueError(
                "Only a Super Admin can delete a Super Admin account."
            )


        # Prevent deleting the last Super Admin
        if user.is_super_admin:

            total = User.query.filter_by(
                role="Super Admin"
            ).count()

            if total <= 1:

                raise ValueError(
                    "The last Super Admin cannot be deleted."
                )


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

        user.set_password(password)

        db.session.commit()

        return user


    # =====================================================
    # Activate User
    # =====================================================

    @staticmethod
    def activate(user):

        user.is_active = True

        db.session.commit()


    # =====================================================
    # Deactivate User
    # =====================================================

    @staticmethod
    def deactivate(user):

        # Only Super Admin can deactivate
        # another Super Admin.
        if (
            user.is_super_admin
            and not current_user.is_super_admin
        ):

            raise ValueError(
                "Only a Super Admin can deactivate a Super Admin account."
            )


        # Don't deactivate the last Super Admin
        if user.is_super_admin:

            total = User.query.filter_by(
                role="Super Admin"
            ).count()

            if total <= 1:

                raise ValueError(
                    "The last Super Admin cannot be deactivated."
                )


        user.is_active = False

        db.session.commit()
        