"""Form object declaration."""
from typing import List, Optional

from flask_wtf import FlaskForm
from starlette_wtf import StarletteForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

from .models import MStatus
from .units import units

class MaterialForm(StarletteForm):
    """
    Material Physical Properties in SI for isotropic material
    """

    name =  StringField('Name', validators=[DataRequired()])
    Tref = FloatField('Tref ' + units['Tref'], validators=[DataRequired()])

    VolumicMass = FloatField('VolumicMass ' + units['VolumicMass'], validators=[DataRequired()])
    SpecificHeat = FloatField('SpecificHeat ' + units['SpecificHeat'], validators=[DataRequired()])

    alpha = FloatField('alpha ' + units['alpha'], validators=[DataRequired()])
    ElectricalConductivity = FloatField('ElectricalConductivity ' + units['ElectricalConductivity'], validators=[DataRequired()])
    ThermalConductivity = FloatField('ThermalConductivity ' + units['ThermalConductivity'], validators=[DataRequired()])
    MagnetPermeability = FloatField('MagnetPermeability', validators=[DataRequired()])

    Young = FloatField('Young ' + units['Young'], validators=[DataRequired()])
    Poisson = FloatField('Poisson', validators=[DataRequired()])
    CoefDilatation = FloatField('CoefDilatation ' + units['CoefDilatation'], validators=[DataRequired()])
    Rpe = FloatField('Rpe ' + units['Rpe'], validators=[DataRequired()])

    nuance = StringField('Nuance', validators=[DataRequired()])
    furnisher = StringField('Furnisher', validators=[DataRequired()])
    ref = StringField('Ref', validators=[DataRequired()])

    # from flask_wtf import FlaskForm, RecaptchaField
    # recaptcha = RecaptchaField()
    ##submit = SubmitField('Submit')

# class MaterialForm(MaterialBaseForm):

status_choices = [
    (MStatus.study, "Study"),
    (MStatus.operation, "Operation"),
    (MStatus.stock, "Stock"),
    (MStatus.defunct, "Defunct")
]

mtype_choices = [
    ("Helix", "Helix"),
    ("Ring", "Ring"),
    ("Lead", "Lead"),
    ("Bitter", "Bitter"),
    ("Supra", "Supra")
]

class MPartForm(StarletteForm):
    """
    MPart 
    """
    name =  StringField('Name', validators=[DataRequired()])

    mtype = StringField('Type', validators=[DataRequired()])
    be = StringField('Be Ref', validators=[DataRequired()])
    geom = StringField('Geom', validators=[DataRequired()])
    status = SelectField('Status', choices=status_choices)

    # TODO mtype part shall not be a choice, it shall be infered by loading geom
    mtype = SelectField('Type', choices=mtype_choices)
    # TODO create liste of materials choice
    # material = SelectField('Material', choices=[MStatus.study, MStatus.operation, MStatus.stock, MStatus.defunct])

class MagnetForm(StarletteForm):
    """
    Magnet 
    """
    name =  StringField('Name', validators=[DataRequired()])

    be = StringField('Be Ref', validators=[DataRequired()])
    geom = StringField('Geom', validators=[DataRequired()])
    status = SelectField('Status', choices=status_choices)

class MSiteForm(StarletteForm):
    """
    Magnet Site
    """
    
    name =  StringField('Name', validators=[DataRequired()])
    conffile: StringField('Conffile', validators=[DataRequired()]) # FileField?? or MultipleFileField??
    status = SelectField('Status', choices=status_choices)


