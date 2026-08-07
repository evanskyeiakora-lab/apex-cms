from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    FileField,
    SubmitField,
    SelectField
)

from wtforms.validators import (
    DataRequired,
    Length,
    Optional
)

from flask_wtf.file import (
    FileAllowed
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
            Optional(),
            Length(max=200)
        ],
        description="Leave blank to generate automatically."
    )

    page_role = SelectField(
        "Page Role",
        choices=[
            ("normal", "Normal Page"),
            ("about-us", "Homepage About-us"),
            ("vision", "Homepage Vision"),
            ("mission", "Homepage Mission"),
            ("history", "Homepage History"),
            ("constitution", "Constitution"),
            ("footer", "Footer Page")
        ],
        default="normal"
    )

    content = TextAreaField(
        "Content",
        validators=[
            DataRequired()
        ]
    )

    featured_image = FileField(
        "Featured Image",
        validators=[
            Optional(),
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Images only."
            )
        ]
    )

    meta_title = StringField(
        "Meta Title",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    meta_description = TextAreaField(
        "Meta Description",
        validators=[
            Optional(),
            Length(max=500)
        ]
    )

    is_published = BooleanField(
        "Publish Page",
        default=True
    )

    submit = SubmitField(
        "Save Page"
    )