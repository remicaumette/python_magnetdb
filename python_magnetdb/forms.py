"""Form object declaration."""
from typing import List, Optional

from flask_wtf import FlaskForm
from starlette_wtf import StarletteForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length


class MaterialForm(StarletteForm):
    """
    Material Physical Properties in SI for isotropic material
    """

    name =  StringField('Name', validators=[DataRequired()])
    Tref = FloatField('Tref', validators=[DataRequired()])

    VolumicMass = FloatField('VolumicMass', validators=[DataRequired()])
    SpecificHeat = FloatField('SpecificHeat', validators=[DataRequired()])

    alpha = FloatField('alpha', validators=[DataRequired()])
    ElectricalConductivity = FloatField('ElectricalConductivity', validators=[DataRequired()])
    ThermalConductivity = FloatField('ThermalConductivity', validators=[DataRequired()])
    MagnetPermeability = FloatField('MagnetPermeability', validators=[DataRequired()])

    Young = FloatField('Young', validators=[DataRequired()])
    Poisson = FloatField('Poisson', validators=[DataRequired()])
    CoefDilatation = FloatField('CoefDilatation', validators=[DataRequired()])
    Rpe = FloatField('Rpe', validators=[DataRequired()])

    nuance = StringField('Nuance', validators=[DataRequired()])
    furnisher = StringField('Furnisher', validators=[DataRequired()])
    ref = StringField('Ref', validators=[DataRequired()])

    # from flask_wtf import FlaskForm, RecaptchaField
    # recaptcha = RecaptchaField()
    ##submit = SubmitField('Submit')

# class MaterialForm(MaterialBaseForm):


