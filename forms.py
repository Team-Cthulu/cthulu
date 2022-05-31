from wtforms import StringField, SubmitField
from wtforms.validators import Length
from flask_wtf import FlaskForm

class OrcSearchForm(FlaskForm):
    query = StringField(
        'Search Orcs', [Length(0, 91, 'Orc name cannot exceed 91 characters.')]
    )
    name = SubmitField('Orc Name')
    reset = SubmitField('Reset')