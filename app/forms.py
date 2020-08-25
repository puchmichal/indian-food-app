from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, URL, NumberRange

from app.utils.data_list_field import DatalistField


class NewRatingForm(FlaskForm):
    """Form for proving feedback about new restaurant or new visit in old restaurant."""

    name = DatalistField("Name", validators=[DataRequired("Please provide name of restaurant")])
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
    spiciness_rating = IntegerField(
        "Spiciness Rating",
        [
            DataRequired(message="Please provide Spiciness rating"),
            NumberRange(min=0, max=5, message="Ratting must be between 0 and 5"),
        ],
    )
    website = StringField("Lunch link", validators=[URL()])
    submit = SubmitField("Submit",)
