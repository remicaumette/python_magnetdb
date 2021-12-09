from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Session, select

from .old_models import MPart, Magnet, MSite, MRecord
from .old_models import MaterialBase, Material, MaterialCreate, MaterialRead
from .old_models import MPartMagnetLink, MagnetMSiteLink
from .old_models import MStatus

from .queries import query_mpart, query_magnet, query_msite, query_material

# TODO:
# so far only Creation, Query
# add method to Read/Display data
# add method to Update and Delete data

# TODO:
# material: use pint for setting properties with units

def create_msite(session: Session, name: str, conffile: str , status: MStatus):
    m1 = MSite(name=name, conffile=conffile, status=status)
    session.add(m1)
    session.commit()
    session.refresh(m1)
    return m1

def create_magnet(session: Session, name: str, be: str, geom: str, status: MStatus, msites: List[MSite]): # msites_id: List[int]):
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


def create_mpart(session: Session, name: str, mtype: str, be: str, geom: str, status: MStatus, magnets: List[Magnet], material: Optional[Material]):
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

def get_magnet_type(session: Session, magnet_id: int ):
    """
    Returns magnet type and the list of mparts attached to this magnet
    """
    objects = get_mparts_mtype(session=session, magnet_id=magnet_id, mtype="Helix")
    if len(objects):
        return ("Insert", objects)
    objects = get_mparts_mtype(session=session, magnet_id=magnet_id, mtype="Bitter")
    if len(objects):
        return ("Bitter", objects)
    objects = get_mparts_mtype(session=session, magnet_id=magnet_id, mtype="Supra")
    if len(objects):
        return ("Supra", objects)

def get_magnet_data(session: Session, magnet_name: str ):
    """
    Get magnet data
    """
    magnet = None
    results = query_magnet(session, magnet_name)
    if not results:
        print("cannot find magnet %s" % magnet_name)
        exit(1)
    else:
        for magnet in results:
            print("magnet:", magnet)
            # objects = get_mparts(session=session, magnet_id=magnet.id)
            # for h in objects:
            #    print(session.get(MPart, h.id).dict())

    mdata = magnet.dict()
    for key in ['be', 'name', 'status', 'id']:
        mdata.pop(key, None)
    for mtype in ["Helix", "Ring", "Lead", "Bitter", "Supra"]:
        if mtype == "Helix":
            # TODO: check Helix type before getting insulator name and data
            results = query_material(session, name="MAT_ISOLANT")
            for material in results:
                insulator_data = material.dict()
                print("insulator_data:", insulator_data)
                # remove uneeded stuff
                for key in ['furnisher', 'ref', 'name', 'id']:
                    insulator_data.pop(key, None)

        objects = get_mparts_mtype(session=session, magnet_id=magnet.id, mtype=mtype)
        for h in objects:
            # get material from material_id
            material = session.get(Material, h.material_id)
            material_data = material.dict()
            # remove uneeded stuff
            for key in ['furnisher', 'ref', 'name', 'id']:
                material_data.pop(key, None)

            if not mtype in mdata:
                mdata[mtype]=[]

            mdata[mtype].append({"geom": h.geom, "material": material_data, "insulator": insulator_data})

    return mdata

def get_msite_data(session: Session, name: str ):
    """
    Generate data for MSite
    """
    results = query_msite(session, name)
    if not results:
        print("cannot find msite %s" % name)
        exit(1)
    else:
        for msite in results:
            print("msite:", msite)

    mdata = msite.dict()

    # hack to export magnets to dict
    mdata['magnets'] = {}
    for magnet in msite.magnets:
        (mtype, objects) = get_magnet_type(session, magnet.id)
        if mtype == "Bitter" or mtype == "Supra":
            mdata['magnets'][magnet.name] = []
            for mpart in objects:
                # TODO remove extension from mpart.geom
                mname = mpart.geom
                yamlfile = mname.rsplit(".yaml", 1)[0]
                mdata['magnets'][magnet.name].append(yamlfile)
        else:
            # TODO remove extension from mpart.geom
            mname = magnet.geom
            yamlfile = mname.rsplit(".yaml", 1)[0]
            mdata['magnets'][magnet.name] = yamlfile

    for key in ['be', 'conffile', 'status', 'id']:
        mdata.pop(key, None)

    return mdata


