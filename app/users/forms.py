from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    BooleanField,
    FileField,
    SubmitField
)

from wtforms.fields import EmailField

from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional
)

from app.utils.constants import Roles


# ==========================================================
# Create User Form
# ==========================================================

class UserForm(FlaskForm):

    first_name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    last_name = StringField(
        "Last Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    email = EmailField(
        "Email Address",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    phone = StringField(
        "Phone Number",
        validators=[
            Optional(),
            Length(max=30)
        ]
    )

    role = SelectField(
        "Role",
        choices=Roles.CHOICES,
        validators=[
            DataRequired()
        ]
    )

    photo = FileField(
        "Profile Photo",
        validators=[
            Optional(),
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Only JPG, JPEG, PNG and WEBP images are allowed."
            )
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(
                min=8,
                message="Password must be at least 8 characters."
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )

    is_active = BooleanField(
        "Active",
        default=True
    )

    submit = SubmitField(
        "Save User"
    )


# ==========================================================
# Edit User Form
# ==========================================================

class EditUserForm(FlaskForm):

    first_name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    last_name = StringField(
        "Last Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    email = EmailField(
        "Email Address",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    phone = StringField(
        "Phone Number",
        validators=[
            Optional(),
            Length(max=30)
        ]
    )

    role = SelectField(
        "Role",
        choices=Roles.CHOICES,
        validators=[
            DataRequired()
        ]
    )

    photo = FileField(
        "Profile Photo",
        validators=[
            Optional(),
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Only JPG, JPEG, PNG and WEBP images are allowed."
            )
        ]
    )

    password = PasswordField(
        "New Password",
        validators=[
            Optional(),
            Length(
                min=8,
                message="Password must be at least 8 characters."
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            Optional(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )

    is_active = BooleanField(
        "Active"
    )

    submit = SubmitField(
        "Update User"
    )


# ==========================================================
# Change Password Form
# ==========================================================

class ChangePasswordForm(FlaskForm):

    current_password = PasswordField(
        "Current Password",
        validators=[
            DataRequired()
        ]
    )

    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(
                min=8,
                message="Password must be at least 8 characters."
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )

    submit = SubmitField(
        "Change Password"
    )