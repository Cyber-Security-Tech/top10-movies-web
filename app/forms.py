"""
forms.py — Flask-WTF form classes for the Top 10 Movies web app.

Defines forms for adding and editing movies.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextAreaField
from wtforms.validators import DataRequired, NumberRange


class AddForm(FlaskForm):
    """
    Form for searching and adding a movie by title.
    """
    title = StringField("Movie Title", validators=[DataRequired(message="Please enter a movie title.")])
    submit = SubmitField("Add Movie")


class EditForm(FlaskForm):
    """
    Form for updating a movie's rating and review.
    """
    rating = FloatField(
        "Your Rating (0 to 10)",
        validators=[
            DataRequired(message="Please enter a numeric rating."),
            NumberRange(min=0, max=10, message="Rating must be between 0 and 10.")
        ]
    )
    review = TextAreaField("Your Review", validators=[DataRequired(message="Please enter a review.")])
    submit = SubmitField("Update Movie")
