from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    BooleanField,
    SubmitField
)
from wtforms.validators import DataRequired, Optional


class MemberForm(FlaskForm):

    full_name = StringField(
        "Full Name",
        validators=[DataRequired()]
    )

    position = StringField(
        "Position",
        validators=[DataRequired()]
    )

    biography = TextAreaField("Biography")

    photo = FileField("Photo")

    email = StringField("Email")

    phone = StringField("Phone")

    facebook = StringField("Facebook")

    linkedin = StringField("LinkedIn")

    twitter = StringField("Twitter / X")

    display_order = IntegerField(
        "Display Order",
        default=1
    )

    is_active = BooleanField(
        "Active",
        default=True
    )

    submit = SubmitField("Save")