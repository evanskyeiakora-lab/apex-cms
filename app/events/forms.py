from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import (
    StringField,
    TextAreaField,
    DateField,
    TimeField,
    IntegerField,
    BooleanField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Optional,
    URL,
    Length,
    NumberRange,
    ValidationError
)

from app.utils.file_upload import allowed_file


class EventForm(FlaskForm):

    title = StringField(
        "Event Title",
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[
            DataRequired(),
            Length(max=5000)
        ]
    )

    featured_image = FileField(
        "Featured Image"
    )

    venue = StringField(
        "Venue",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    start_date = DateField(
        "Start Date",
        format="%Y-%m-%d",
        validators=[DataRequired()]
    )

    end_date = DateField(
        "End Date",
        format="%Y-%m-%d",
        validators=[Optional()]
    )

    start_time = TimeField(
        "Start Time",
        format="%H:%M",
        validators=[Optional()]
    )

    end_time = TimeField(
        "End Time",
        format="%H:%M",
        validators=[Optional()]
    )

    organizer = StringField(
        "Organizer",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    registration_link = StringField(
        "Registration Link",
        validators=[
            Optional(),
            Length(max=500),
            URL(message="Please enter a valid URL.")
        ]
    )

    display_order = IntegerField(
        "Display Order",
        default=0,
        validators=[
            NumberRange(min=0)
        ]
    )

    is_featured = BooleanField(
        "Featured Event"
    )

    is_published = BooleanField(
        "Published",
        default=True
    )

    submit = SubmitField(
        "Save Event"
    )

    def validate_featured_image(self, field):
        if field.data and field.data.filename:
            if not allowed_file(field.data.filename):
                raise ValidationError(
                    "Only JPG, JPEG, PNG and WEBP images are allowed."
                )

    def validate_end_date(self, field):

        if (
            self.start_date.data
            and field.data
            and field.data < self.start_date.data
        ):
            raise ValidationError(
                "End date cannot be earlier than the start date."
            )

    def validate_end_time(self, field):

        if (
            self.start_date.data
            and self.end_date.data
            and self.start_date.data == self.end_date.data
            and self.start_time.data
            and field.data
            and field.data <= self.start_time.data
        ):
            raise ValidationError(
                "End time must be later than the start time."
            )