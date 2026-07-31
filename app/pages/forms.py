from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length
)


class PageForm(FlaskForm):

    title = StringField(
        "Page Title",
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )

    slug = StringField(
        "Slug",
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )

    content = TextAreaField(
        "Content",
        validators=[DataRequired()]
    )

    featured_image = FileField(
        "Featured Image",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Images only!"
            )
        ]
    )

    meta_title = StringField(
        "Meta Title"
    )

    meta_description = TextAreaField(
        "Meta Description"
    )

    is_published = BooleanField(
        "Published",
        default=True
    )

    submit = SubmitField(
        "Save Page"
    )