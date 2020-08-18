from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, URL, NumberRange


class NewRatingForm(FlaskForm):
    """Form for proving feedback about new restaurant or new visit in old restaurant."""

    name = StringField("Name", [DataRequired("Please provide name of restaurant")])
    delivery_rating = IntegerField(
        "Delivery Rating",
        [
            DataRequired(message="Please provide delivery rating"),
            NumberRange(min=0, max=5, message="Ratting must be between 0 and 5"),
        ],
    )
    taste_rating = IntegerField(
        "Taste Rating",
        [
            DataRequired(message="Please provide taste rating"),
            NumberRange(min=0, max=5, message="Ratting must be between 0 and 5"),
        ],
    )
    website = StringField("Lunch link", validators=[URL()])
    submit = SubmitField("Submit",)
