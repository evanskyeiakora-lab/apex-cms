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

        # Check username
        if User.query.filter_by(
            username=form.username.data
        ).first():
            raise ValueError(
                "Username already exists."
            )

        # Check email
        if User.query.filter_by(
            email=form.email.data
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
            phone=form.phone.data.strip()
            if form.phone.data else None,
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

        # Check username
        existing = User.query.filter_by(
            username=form.username.data
        ).first()

        if existing and existing.id != user.id:
            raise ValueError(
                "Username already exists."
            )

        # Check email
        existing = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing and existing.id != user.id:
            raise ValueError(
                "Email address already exists."
            )

        user.first_name = form.first_name.data.strip()
        user.last_name = form.last_name.data.strip()
        user.username = form.username.data.strip()
        user.email = form.email.data.strip().lower()
        user.phone = (
            form.phone.data.strip()
            if form.phone.data else None
        )

        if allow_role_change:
            user.role = form.role.data

        user.is_active = form.is_active.data

        if form.photo.data:
            filename = save_image(
                form.photo.data,
                USERS_FOLDER
            )
            user.photo = filename

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

        from flask_login import current_user

        # Prevent deleting yourself
        if current_user.id == user.id:
            raise ValueError(
                "You cannot delete your own account."
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