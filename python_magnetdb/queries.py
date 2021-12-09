from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Session, select

from .old_models import MPart, Magnet, MSite, MRecord
from .old_models import MaterialBase, Material, MaterialCreate, MaterialRead
from .old_models import MPartMagnetLink, MagnetMSiteLink
from .old_models import MStatus

def query_material(session: Session, name: str):
    statement = select(Material).where(Material.name == name)
    results = session.exec(statement)
    return results

def query_mpart(session: Session, name: str):
    statement = select(MPart).where(MPart.name == name)
    results = session.exec(statement)
    return results

def query_magnet(session: Session, name: str):
    statement = select(Magnet).where(Magnet.name == name)
    results = session.exec(statement)
    return results

def query_msite(session: Session, name: str):
    statement = select(MSite).where(MSite.name == name)
    results = session.exec(statement)
    return results

