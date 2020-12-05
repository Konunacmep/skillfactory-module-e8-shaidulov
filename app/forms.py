from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class SiteForm(FlaskForm):
    sites = TextAreaField('Введите адреса сайтов, можно несколько, разделив запятой', validators=[DataRequired()])
    submit = SubmitField('OK')
