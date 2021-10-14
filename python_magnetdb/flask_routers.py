from typing import TYPE_CHECKING, List, Optional

from flask import Blueprint
from flask import Flask, flash, url_for, escape, request, redirect, render_template

from sqlmodel import Session, select

from .database import create_db_and_tables, engine, get_session
from .models import MPartBase, MPart, MPartCreate, MPartRead, MPartUpdate
from .models import MagnetBase, Magnet, MagnetCreate, MagnetRead, MagnetUpdate 
from .models import MSiteBase, MSite, MSiteCreate, MSiteRead, MSiteUpdate
from .models import MRecordBase, MRecord, MRecordCreate, MRecordRead, MRecordUpdate
from .models import MaterialBase, Material, MaterialCreate, MaterialRead, MaterialUpdate
from .models import MagnetReadWithMSite, MSiteReadWithMagnets
from .models import MPartReadWithMagnet
from . import crud

from . import forms


urls_blueprint = Blueprint('urls', __name__,)

@urls_blueprint.route('/')
def index():
    #return f'Bienvenue dans MagnetDB'
    return render_template('index.html')
    
@urls_blueprint.route('/materials')
def list():
    with Session(engine) as session:
        statement = select(Material)
        materials = session.exec(statement).all()
    return render_template('materials/list.html', materials=materials)

@urls_blueprint.route('/material/<int:id>')
def view(id: int):
    with Session(engine) as session:
        material = session.get(Material, id)
        data = material.dict()
        data.pop('id', None)        
        
        return render_template('materials/view.html', material=data, material_id=material.id)

@urls_blueprint.route('/material/update', methods=["GET", "POST"])
def update():
    return f"Update Material"
    """
    print("update:", id)
    with Session(engine) as session:
        material = session.get(Material, id)
        data = material.dict()
        data.pop('id', None)        
        
        print(request.method)
        if request.method == "POST":
            req = request.form
            return redirect(request.url)
        
        return render_template('materials/update.html', material=data)
    """

@urls_blueprint.route('/submit/<int:id>', methods=['GET', 'POST'])
def submit(id: int):
    with Session(engine) as session:
        material = session.get(Material, id)
        print("update: input", material)
    
        form = forms.MaterialForm(obj=material)
        if form.validate_on_submit():
            print("Material update validated")
            flash('Material has been updated')

            # shall get MaterialBaseForm from form
            form.populate_obj(material)
            print("update output:", material)
            session.commit()
            session.refresh(material)
            return redirect(url_for('urls.index'))
        else:
            print("Material update not validated")
            print("errors:", form.errors)
        
    return render_template('submit.html', form=form, id=id)

@urls_blueprint.route('/magnets')
def list_magnets():
    with Session(engine) as session:
        statement = select(Magnet)
        magnets = session.exec(statement).all()
    return render_template('magnets/list.html', magnets=magnets)

@urls_blueprint.route('/magnet/<int:id>')
def view_magnets(id: int):
    with Session(engine) as session:
        magnet = session.get(Magnet, id)
        data = magnet.dict()
        data.pop('id', None)
        data["MParts"] = []
        for magnet in magnet.mparts:
            data["MParts"].append(magnet.name)
        return render_template('magnets/view.html', magnet=data)

@urls_blueprint.route('/msites')
def list_msites():
    with Session(engine) as session:
        statement = select(MSite)
        msites = session.exec(statement).all()
    return render_template('msites/list.html', msites=msites)

@urls_blueprint.route('/msite/<int:id>')
def view_msites(id: int):
    with Session(engine) as session:
        msite = session.get(MSite, id)
        data = msite.dict()
        print("blueprint:", data)
        data.pop('id', None)
        data["Magnets"] = []
        for magnet in msite.magnets:
            data["Magnets"].append(magnet.name)
        return render_template('msites/view.html', msite=data)

@urls_blueprint.route('/mparts')
def list_mparts():
    with Session(engine) as session:
        statement = select(MPart)
        mparts = session.exec(statement).all()
    return render_template('mparts/list.html', mparts=mparts)

@urls_blueprint.route('/mpart/<int:id>', methods=['GET', 'POST'])
def view_mparts(id: int):
    with Session(engine) as session:
        mpart = session.get(MPart, id)
        data = mpart.dict()
        data.pop('id', None)
        data['Material'] = session.get(Material, mpart.material_id).name
        data.pop('material_id', None)
        return render_template('mparts/view.html', mpart=data)

@urls_blueprint.route('/mrecords')
def list_mrecords():
    with Session(engine) as session:
        statement = select(MRecord)
        mrecords = session.exec(statement).all()
    return render_template('mrecords/list.html', mrecords=mrecords)

@urls_blueprint.route('/mrecord/<int:id>')
def view_mrecords(id: int):
    with Session(engine) as session:
        mrecord = session.get(MRecord, id)
        data = mrecord.dict()
        data.pop('id', None)
        return render_template('mrecords/view.html', mrecord=data)
