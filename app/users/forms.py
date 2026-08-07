from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SelectField,
    BooleanField,
    FileField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional
)

from flask_wtf.file import FileAllowed


ROLE_CHOICES = [
    ("Super Admin", "Super Admin"),
    ("Administrator", "Administrator"),
    ("Editor", "Editor"),
    ("Author", "Author"),
    ("Moderator", "Moderator"),
]


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

    email = StringField(
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
        choices=ROLE_CHOICES,
        validators=[DataRequired()]
    )

    photo = FileField(
        "Profile Photo",
        validators=[
            Optional(),
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Images only."
            )
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8)
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


class ChangePasswordForm(FlaskForm):

    current_password = PasswordField(
        "Current Password",
        validators=[DataRequired()]
    )

    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=8)
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

    submit = SubmitField(
        "Change Password"
    )