from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Session, select

from .models import MPart, Magnet, MSite, MRecord
from .models import MaterialBase, Material, MaterialCreate, MaterialRead
from .models import MPartMagnetLink, MagnetMSiteLink

# TODO:
# so far only Creation, Query 
# add method to Read/Display data
# add method to Update and Delete data

# TODO:
# material: use pint for setting properties with units

def create_msite(session: Session, name: str, conffile: str , status: str):
    m1 = MSite(name=name, conffile=conffile, status=status)
    session.add(m1)
    session.commit()
    session.refresh(m1)
    return m1

def create_magnet(session: Session, name: str, be: str, geom: str, status: str, msites: List[MSite]): # msites_id: List[int]):
    """
    msites: List[MSite] = []
    for id in msites_id:
        msites.append( session.get(MSite, id) )
    """
    magnet = Magnet(name=name, be=be, geom=geom, status=status, msites=msites)
    session.add(magnet)
    session.commit()
    session.refresh(magnet)
    return magnet

def create_mpart(session: Session, name: str, type: str, be: str, geom: str, status: str, magnets: List[Magnet], material: Material):
    # TODO get material_id from material name
    part = MPart(name=name, type=type, be=be, geom=geom, status=status, material_id=material.id, magnets=magnets)
    session.add(part)
    session.commit()
    session.refresh(part)
    return part

def create_material(session: Session, name: str, ElectricalConductivity: float, Rpe: float, nuance: Optional[str] = None):
    """
    TODO: use pint to get values in SI
    """
    material = Material(name=name, ElectricalConductivity=ElectricalConductivity, Rpe=Rpe, nuance=nuance)
    session.add(material)
    session.commit()
    session.refresh(material)
    return material
    
def query_msite(session: Session, name: str):
    statement = select(MSite).where(MSite.name == name)
    results = session.exec(statement)
    return results

def query_material(session: Session, name: str):
    statement = select(Material).where(Material.name == name)
    results = session.exec(statement)
    return results

def query_magnet(session: Session, name: str):
    statement = select(Magnet).where(Magnet.name == name)
    results = session.exec(statement)
    return results


def get_magnets(session: Session, site_id: int):   
    statement = select(MagnetMSiteLink).where(MagnetMSiteLink.msite_id == site_id)
    results = session.exec(statement)
    return results

def get_mparts(session: Session, magnet_id: int):   
    """
    get all parts from a magnet
    """
    statement = select(MPartMagnetLink).where(MPartMagnetLink.magnet_id == magnet_id)
    results = session.exec(statement)
    return results

def get_mparts_type(session: Session, magnet_id: int, type: str):   
    """
    get all parts from a magnet
    """
    statement = select(MPart, MPartMagnetLink).join(MPart).where(MPartMagnetLink.magnet_id == magnet_id).where(MPart.type == type)
    results = session.exec(statement)
    selected = []
    for part, link in results:
        selected.append(part)
    return selected

def get_mpart_history(session: Session, mpart_id: id):
    """
    get list of magnets in which mpart is present
    """
    statement = select(Magnet, MPartMagnetLink).join(Magnet).where(MPartMagnetLink.mpart_id == mpart_id)
    results = session.exec(statement)
    selected = []
    for magnet, link in results:
        selected.append(magnet)
    return selected

def get_magnet_history(session: Session, msite_id: id):
    """
    get list of sites in which magnet is present
    """
    statement = select(MSite, MagnetMSiteLink).join(MSite).where(MagnetMSiteLink.msite_id == msite_id)
    results = session.exec(statement)
    selected = []
    for msite, link in results:
        selected.append(msite)
    return selected



