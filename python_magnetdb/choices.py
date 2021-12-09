from sqlmodel import Session, select

from sqlmodel import Session, select

from .crud import get_magnet_type
from .database import engine
from .old_models import MPart, Magnet, MSite
from .old_models import MStatus
from .old_models import Material
from .units import units


def material_choices():
    with Session(engine) as session:
        statement = select(Material)
        results = session.exec(statement).all()

    choices = []
    for obj in results:
        desc = obj.name + " (" + obj.nuance + "," + "Rpe:" + str(obj.Rpe) + units['Rpe'] + ")"
        choices.append( (obj.id, desc))

    return choices

def mpart_choices(mtype: str, status: MStatus):
    with Session(engine) as session:
        statement = select(MPart).where(MPart.mtype == mtype).where(MPart.status == status)
        results = session.exec(statement).all()

    choices = []
    for obj in results:
        desc = obj.name

        # Get Material
        material = select(Material).where(Material.id == obj.material_id)
        desc += " (" + material.name + ":" + obj.nuance + "," + "Rpe:" + obj.rpe + units['Rpe'] + ")"

        # TODO load obj.geom to get basic geom infos
        # geom = yaml.load(open(obj.name, 'r'))

        choices.append( (obj, desc))

    return choices

def magnet_choices(status: MStatus):
    with Session(engine) as session:
        statement = select(Magnet).where(Magnet.status == status)
        results = session.exec(statement).all()

    choices = []
    for obj in results:
        desc = obj.name

        # TODO add magnet type (aka Insert, Bitter or Supra)
        (mtype, components) = get_magnet_type(obj.id)
        desc += "(" + mtype + ")"

        # TODO load obj.geom to get basic geom infos (aka inner/outer diameter)
        # geom = yaml.load(open(obj.name, 'r'))

        choices.append( (obj, desc))

    return choices

def msite_choices(status: MStatus):
    with Session(engine) as session:
        statement = select(MSite).where(MSite.status == status)
        results = session.exec(statement).all()

    choices = []
    for obj in results:
        desc = obj.name

        # TODO add msite composition (aka Insert + Bitter + Supra)
        desc += "("
        for magnet in obj.magnets:
            (mtype, components) = get_magnet_type(magnet.id)
            desc += magnet.name + ":" + mtype + "," + len(components) + " objects, "
        # TODO remove last ','
        last_char_index = desc.rfind(',')
        desc = desc[:last_char_index] + "," + desc[last_char_index+1:]
        desc += ")"

        choices.append( (obj, desc))

    return choices
