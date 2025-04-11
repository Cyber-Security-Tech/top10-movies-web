from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

class AddForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")

class EditForm(FlaskForm):
    rating = FloatField("Your Rating (0–10)", validators=[DataRequired(), NumberRange(min=0, max=10)])
    review = TextAreaField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Save Changes")
