from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    BooleanField,
    SubmitField
)

from wtforms.validators import DataRequired


class HeroForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[DataRequired()]
    )

    subtitle = TextAreaField(
        "Subtitle"
    )

    image = FileField(
        "Hero Image",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Images only!"
            )
        ]
    )

    button_text = StringField(
        "Button Text"
    )

    button_url = StringField(
        "Button URL"
    )

    display_order = IntegerField(
        "Display Order",
        default=1
    )

    is_active = BooleanField(
        "Active",
        default=True
    )

    submit = SubmitField(
        "Save Slide"
    )