from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextAreaField
from wtforms.validators import InputRequired, NumberRange, DataRequired

class AddForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")

class EditForm(FlaskForm):
    rating = FloatField("Your Rating Out of 10 (e.g. 8.5)", validators=[
        InputRequired(message="Please enter a numeric rating."),
        NumberRange(min=0, max=10, message="Rating must be between 0 and 10.")
    ])
    review = TextAreaField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Update Movie")
