from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    IntegerField,
    BooleanField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Optional,
    Length,
    NumberRange,
    ValidationError
)

from app.utils.file_upload import allowed_file


class GalleryForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[
            DataRequired(),
            Length(max=255)
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[
            Optional(),
            Length(max=5000)
        ]
    )

    image = FileField(
        "Gallery Image"
    )

    category = SelectField(
        "Category",
        choices=[
            ("General", "General"),
            ("Church Service", "Church Service"),
            ("Conference", "Conference"),
            ("Youth Ministry", "Youth Ministry"),
            ("Women's Ministry", "Women's Ministry"),
            ("Men's Ministry", "Men's Ministry"),
            ("Children", "Children"),
            ("Outreach", "Outreach"),
            ("Community", "Community")
        ],
        validators=[DataRequired()]
    )

    display_order = IntegerField(
        "Display Order",
        default=0,
        validators=[
            NumberRange(
                min=0,
                message="Display order cannot be negative."
            )
        ]
    )

    is_featured = BooleanField(
        "Featured Image"
    )

    # Keep this if your Gallery model still uses is_active
    is_active = BooleanField(
        "Active",
        default=True
    )

    # Uncomment this instead if you've switched to PublishMixin
    #
    # status = SelectField(
    #     "Status",
    #     choices=[
    #         ("draft", "Draft"),
    #         ("published", "Published"),
    #         ("archived", "Archived")
    #     ],
    #     default="published"
    # )

    submit = SubmitField(
        "Save Gallery"
    )

    # -----------------------------
    # Image Validation
    # -----------------------------
    def validate_image(self, field):

        if field.data and field.data.filename:

            if not allowed_file(field.data.filename):

                raise ValidationError(
                    "Only JPG, JPEG, PNG and WEBP images are allowed."
                )