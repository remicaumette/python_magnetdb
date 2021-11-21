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

@urls_blueprint.route('/msites.html')
def msites_menu():
    return render_template('msites.html')

@urls_blueprint.route('/mparts.html')
def mparts_menu():
    return render_template('mparts.html')

@urls_blueprint.route('/mrecords.html')
def mrecords_menu():
    return render_template('mrecords.html')



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
