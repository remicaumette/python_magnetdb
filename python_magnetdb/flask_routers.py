from typing import TYPE_CHECKING, List, Optional

from flask import Blueprint
from flask import Flask, escape, request, render_template

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

urls_blueprint = Blueprint('urls', __name__,)


@urls_blueprint.route('/')
def index():
    return 'urls index route'
    
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
        print("blueprint:", data)
        return render_template('materials/view.html', material=data)

    
"""
@flask_app.route("/")
def flask_main():
    name = request.args.get("name", "World")
    return f"Hello, {escape(name)} from Flask!"

@flask_app.route("/tutu")
def flask_tutu():
    return f"Tutu from Flask!"

import pandas as pd
@flask_app.route("/material", methods=['GET'])
def read_materials(*, session: Session = Depends(get_session), ):
    statement = select(Material)
    materials = session.exec(statement).all()
    return materials
"""

"""
import pandas as pd
@flask_app.route("/material", methods=['GET'])
def flask_material():
    data_dic = {
        'id': [100, 101, 102],
        'color': ['red', 'blue', 'red']}
    columns = ['id', 'color']
    index = ['a', 'b', 'c']

    df = pd.DataFrame(data_dic, columns=columns, index=index)
    table = df.to_html(index=False)
    return render_template("at-leaderboard.html", table=table)
"""
