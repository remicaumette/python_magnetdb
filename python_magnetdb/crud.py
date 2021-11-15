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

def duplicate_magnet(session: Session, iname: str, oname: str ):
    msites : List[MSite] = []
    results = query_magnet(session, iname)
    for imagnet in results:
        print(imagnet)
        mparts = get_mparts(session, imagnet.id)

        magnet = Magnet(name=oname, be=imagnet.be, geom=imagnet.geom, status=imagnet.status, msites=msites)
        magnet.mparts = imagnet.mparts
        session.add(magnet)
        session.commit()
        session.refresh(magnet)

    # ??is this needed??
    # get mpart from imagnet and update mpart
    """
    for part in mparts:
        if not magnet in part.magnets:
            part.magnets.append(magnet)
        session.refresh(part)
    """
    return magnet

def magnet_add_mpart(session: Session, magnet: Magnet, mpart: MPart ):
    mpart.magnets.append(magnet)
    # magnet.mparts.append(MPart)
    session.commit()
    # session.refresh(magnet)
    session.refresh(mpart)
    pass 

def magnet_delete_mpart(session: Session, magnet: Magnet, mpart: MPart ):
    mpart.magnets.remove(magnet)
    # magnet.mparts.remove(MPart)
    session.commit()
    # session.refresh(magnet)
    session.refresh(mpart)
    pass 

def magnet_replace_mpart(session: Session, name: str, impart: str, ompart: str ):
    results = query_magnet(session, name)
    for magnet in results:
        print(magnet)
        
        # remove impart from magnet
        res_parts = query_mpart(session, impart)
        for part in res_parts:
            magnet_delete_mpart(session, magnet, part)
        
        # add ompart to magnet
        res_parts = query_mpart(session, ompart)
        for part in res_parts:
            magnet_add_mpart(session, magnet, part)
    pass 

def magnet_add_msite(session: Session, magnet: Magnet, msite: MSite ):
    msite.magnets.append(magnet)
    session.commit()
    session.refresh(msite)
    pass 

def magnet_delete_msite(session: Session, magnet: Magnet, msite: MSite ):
    msite.magnets.remove(magnet)
    session.commit()
    session.refresh(msite)
    pass 

def duplicate_site(session: Session, iname: str, oname: str ):
    results = query_msite(session, iname)
    for isite in results:
        print(isite)
        magnets = get_magnets(session, isite.id)

        site = MSite(name=oname, conffile="", status="New")
        site.magnets = isite.magnets
        session.add(site)
        session.commit()
        session.refresh(site)

    # ??is this needed??
    # get mpart from imagnet and update mpart
    """
    for part in mparts:
        if not magnet in part.magnets:
            part.magnets.append(magnet)
        session.refresh(part)
    """
    return site

def create_mpart(session: Session, name: str, mtype: str, be: str, geom: str, status: str, magnets: List[Magnet], material: Optional[Material]):
    # TODO get material_id from material name
    part = MPart(name=name, mtype=mtype, be=be, geom=geom, status=status, material_id=material.id, magnets=magnets)
    session.add(part)
    session.commit()
    session.refresh(part)
    return part

def create_material(session: Session, name: str, ElectricalConductivity: float, Rpe: float,
                    Tref: Optional[float], VolumicMass: Optional[float], SpecificHeat: Optional[float], alpha: Optional[float],
                    ThermalConductivity: Optional[float], MagnetPermeability: Optional[float], Young: Optional[float],
                    Poisson: Optional[float], CoefDilatation: Optional[float], nuance: Optional[str] = None):
    """
    TODO: use pint to get values in SI
    """
    
    material = Material(name=name, ElectricalConductivity=ElectricalConductivity, Rpe=Rpe, Tref=Tref, VolumicMass=VolumicMass,
                    SpecificHeat=SpecificHeat, alpha=alpha, ThermalConductivity=ThermalConductivity, MagnetPermeability=MagnetPermeability,
                    Young=Young, Poisson=Poisson, CoefDilatation=CoefDilatation, nuance=nuance)
    
    session.add(material)
    session.commit()
    session.refresh(material)
    return material
    
def query_msite(session: Session, name: str):
    statement = select(MSite).where(MSite.name == name)
    results = session.exec(statement)
    return results

def check_material(session: Session, id: int):
    """
    Check if properties are defined for Material with id
    """
    material = session.get(Material, id)
    data = material.dict()
    defined =  material.dict(exclude_defaults=True)
    undef_set = set(data.keys()) - set(defined.keys())
    return undef_set
    
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

def get_magnets(session: Session, site_id: int):   
    statement = select(MagnetMSiteLink).where(MagnetMSiteLink.msite_id == site_id)
    results = session.exec(statement)
    return results

def get_mparts(session: Session, magnet_id: int):   
    """
    get all parts from a magnet
    """
    statement = select(MPart, MPartMagnetLink).join(MPart).where(MPartMagnetLink.magnet_id == magnet_id)
    results = session.exec(statement)
    selected = []
    for part, link in results:
        selected.append(part)
    return selected

def get_mparts_mtype(session: Session, magnet_id: int, mtype: str):   
    """
    get all parts from a magnet
    """
    statement = select(MPart, MPartMagnetLink).join(MPart).where(MPartMagnetLink.magnet_id == magnet_id).where(MPart.mtype == mtype)
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



