"""Form object declaration."""
from typing import List, Optional

from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length


class MaterialForm(FlaskForm):
    """
    Material Physical Properties in SI for isotropic material
    """
    
    name =  StringField('Name', validators=[DataRequired()])

    # from flask_wtf import FlaskForm, RecaptchaField
    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
    