from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PropertyForm(FlaskForm):
    property1 = StringField("property1",validators=[DataRequired()])
    property2 = StringField("property2",validators=[DataRequired()])
    property3 = StringField("property3",validators=[DataRequired()])
    property4 = StringField("property4",validators=[DataRequired()])
    submit = SubmitField("submit")