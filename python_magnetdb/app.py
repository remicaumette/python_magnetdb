from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Session, select

from .database import create_db_and_tables, engine
from .models import MPart, Magnet, MSite, MRecord
from .models import MaterialBase, Material, MaterialCreate, MaterialRead
from .models import MPartMagnetLink, MagnetMSiteLink

from .crud import *
import json

# def get_parts(session: Session, magnet_id: int):   
#     data = {}
#     mparts = get_mparts(session, magnet_id)
#     for part in mparts:
#         mpart = session.get(MPart, part.mpart_id)
#         print(mpart.dict())
#         material = session.get(Material, mpart.material_id)
#         mdata = material.dict()
#         #
#         # discard data from MaterialRef

def main():
    create_db_and_tables()

# TODO: how to create objects
# create materials
# create site
# create magnet with a link to site
# create parts for a magnet

# WORKFLOWS
# add a new site:
# if magnet exist, update magnet (aka add miste to msites)
# else
#   add new magnet:
#   if part exist, update part (aka add magnet to magnets)
#   else
#       create part
#       if material exist
#       otherwise create material

# change site status:

# TODO: create a clip.py

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--createdb", help="createdb", action='store_true')
    parser.add_argument("--createsite", help="createsite", action='store_true')
    parser.add_argument("--displaymagnet", help="display magnet", type=str, default=None)
    args = parser.parse_args()

    if args.createdb:
        main()

    if args.createsite:
        with Session(engine) as session:
            m1 = create_msite(session=session, name="M19061901", conffile="MAGFILE2019.06.20.35T.conf", status="On")
        
            Helices = create_magnet(session=session, name="HL-34", be="HL-34-001-A", geom="HL-31.yaml", status="On", msites=[m1])
            Bitters = create_magnet(session=session, name="M9Bitters", be="B_XYZ", geom="Bitters.yaml", status="On", msites=[m1])
        
            H1 = create_material(session=session, name="MA15101601", nuance="Cu5Ag5,08", Rpe=481e+6, ElectricalConductivity=52.4e+6)
            H2 = create_material(session=session, name="MA15061703", nuance="Cu5Ag5,65", Rpe=482e+6, ElectricalConductivity=53.3e+6)
            H3 = create_material(session=session, name="MA15061801", nuance="Cu5Ag5,65", Rpe=496e+6, ElectricalConductivity=52.6e+6)
            H4 = create_material(session=session, name="MA15101501", nuance="Cu5Ag5,08", Rpe=508e+6, ElectricalConductivity=52.8e+6)
            H5 = create_material(session=session, name="MA15101501", nuance="Cu5Ag5,08", Rpe=506e+6, ElectricalConductivity=53.1e+6)
            H6 = create_material(session=session, name="MA18060101", nuance="Cu5Ag5,35", Rpe=0, ElectricalConductivity=53.2e+6)
            H7 = create_material(session=session, name="MA18012501", nuance="Cu5Ag5,09", Rpe=0, ElectricalConductivity=53.1e+6)
            H8 = create_material(session=session, name="MA18051801", nuance="Cu5Ag5,22", Rpe=0, ElectricalConductivity=51.9e+6)
            H9 = create_material(session=session, name="MA18101201", nuance="Cu5Ag5,08", Rpe=0, ElectricalConductivity=53.7e+6)
            H10 = create_material(session=session, name="MA18110501", nuance="Cu5Ag5,08", Rpe=0, ElectricalConductivity=53.3e+6)
            H11 = create_material(session=session, name="MA19012101", nuance="Cu5Ag5,5", Rpe=0, ElectricalConductivity=53.8e+6)
            H12 = create_material(session=session, name="MA19011601", nuance="Cu5Ag5,5", Rpe=0, ElectricalConductivity=53.2e+6)
            H13 = create_material(session=session, name="MA10061702", nuance="CuCrZr", Rpe=366e+6, ElectricalConductivity=46.5e+6)
            H14 = create_material(session=session, name="MA10061703", nuance="CuCrZr", Rpe=373e+6, ElectricalConductivity=50.25e+6)
        
            create_mpart(session=session, name='H15101601', type='Helix', be='HL-34-001-A', geom='HL-31_H1.yaml', status='On', magnets=[Helices], material=H1)
            create_mpart(session=session, name='H15061703', type='Helix', be='HL-34-003-A', geom='HL-31_H2.yaml', status='On', magnets=[Helices], material=H2)
            create_mpart(session=session, name='H15061801', type='Helix', be='HL-34-005-A', geom='HL-31_H3.yaml', status='On', magnets=[Helices], material=H3)
            create_mpart(session=session, name='H15101501', type='Helix', be='HL-34-007-A', geom='HL-31_H4.yaml', status='On', magnets=[Helices], material=H4)
            create_mpart(session=session, name="H15101501", type='Helix', be='HL-34-009-A', geom='HL-31_H5.yaml', status='On', magnets=[Helices], material=H5)
            create_mpart(session=session, name="H18060101", type='Helix', be='HL-34-011-A', geom='HL-31_H6.yaml', status='On', magnets=[Helices], material=H6)
            create_mpart(session=session, name="H18012501", type='Helix', be='HL-34-013-A', geom='HL-31_H7.yaml', status='On', magnets=[Helices], material=H7)
            create_mpart(session=session, name="H18051801", type='Helix', be='HL-34-015-A', geom='HL-31_H8.yaml', status='On', magnets=[Helices], material=H8)
            create_mpart(session=session, name="H18101201", type='Helix', be='HL-34-017', geom='HL-31_H9.yaml', status='On', magnets=[Helices], material=H9)
            create_mpart(session=session, name="H18110501", type='Helix', be='HL-34-019', geom='HL-31_H10.yaml', status='On', magnets=[Helices], material=H10)
            create_mpart(session=session, name="H19012101", type='Helix', be='HL-34-021', geom='HL-31_H11.yaml', status='On', magnets=[Helices], material=H11)
            create_mpart(session=session, name="H19011601", type='Helix', be='HL-34-023', geom='HL-31_H12.yaml', status='On', magnets=[Helices], material=H12)
            create_mpart(session=session, name="H10061702", type='Helix', be='HR-21-125-A', geom='HL-31_H13.yaml', status='On', magnets=[Helices], material=H13)
            create_mpart(session=session, name="H10061703", type='Helix', be='HR-21-127-A', geom='HL-31_H14.yaml', status='On', magnets=[Helices], material=H4)

            # Rings
            R1 = create_material(session=session, name="MA20072301", nuance="CuNiBe", Rpe=568e+6, ElectricalConductivity=0)
            R2 = create_material(session=session, name="MA20072304", nuance="CuCrZr", Rpe=324e+6, ElectricalConductivity=0)
            R3 = create_material(session=session, name="MA20072302", nuance="CuCrZr", Rpe=343e+6, ElectricalConductivity=80) # !! % IACS
            R4 = create_material(session=session, name="MA20072303", nuance="CuCrZr", Rpe=357e+6, ElectricalConductivity=81.7) # !! % IACS
            R5 = create_material(session=session, name="MA21040901", nuance="CuCrZr", Rpe=0, ElectricalConductivity=0)
            R6 = create_material(session=session, name="MARING", nuance="CuCrZr", Rpe=0, ElectricalConductivity=0)

            create_mpart(session=session, name="B20061903", type='Ring', be='HL-27-029-G', geom='Ring-H1H2.yaml', status='On', magnets=[Helices], material=R1)
            create_mpart(session=session, name="B20061904", type='Ring', be='HL-27-030-D', geom='Ring-H2H3.yaml', status='On', magnets=[Helices], material=R2)
            create_mpart(session=session, name="B20061901", type='Ring', be='HL-27-031-C', geom='Ring-H3H4.yaml', status='On', magnets=[Helices], material=R3)
            create_mpart(session=session, name="B20061902", type='Ring', be='HL-27-032-C', geom='Ring-H4H5.yaml', status='On', magnets=[Helices], material=R4)
            create_mpart(session=session, name="B20061902", type='Ring', be='HL-27-033-C', geom='Ring-H5H6.yaml', status='On', magnets=[Helices], material=R5)
            create_mpart(session=session, name="B21040901", type='Ring', be='HL-27-034-C', geom='Ring-H6H7.yaml', status='On', magnets=[Helices], material=R6)
            create_mpart(session=session, name="B21040901", type='Ring', be='HL-27-035-C', geom='Ring-H7H8.yaml', status='On', magnets=[Helices], material=R6)
            create_mpart(session=session, name="B21040901", type='Ring', be='HL-27-036-C', geom='Ring-H8H9.yaml', status='On', magnets=[Helices], material=R6)
            create_mpart(session=session, name="B21040901", type='Ring', be='HL-27-037-C', geom='Ring-H9H10.yaml', status='On', magnets=[Helices], material=R6)
            create_mpart(session=session, name="B21040901", type='Ring', be='HL-27-038-C', geom='Ring-H10H11.yaml', status='On', magnets=[Helices], material=R6)
            create_mpart(session=session, name="B21040901", type='Ring', be='HL-27-039-C', geom='Ring-H11H12.yaml', status='On', magnets=[Helices], material=R6)
            create_mpart(session=session, name="B21040901", type='Ring', be='HL-27-040-C', geom='Ring-H12H13.yaml', status='On', magnets=[Helices], material=R6)
            create_mpart(session=session, name="B21040901", type='Ring', be='HL-27-041-C', geom='Ring-H13H14.yaml', status='On', magnets=[Helices], material=R6)

            # Rings: HL-27-xx
            # 029 030 031  032 033 034 035 036 037 038 039 040 041
            # BP  HP  HP   BP  HP  BP  HP  BP  HP  BP  HP  BP  HP
        
            # CurrentLeads
            L1 = create_material(session=session, name="MALINNER", nuance="Cu", Rpe=0, ElectricalConductivity=58.0e+6)
            L2 = create_material(session=session, name="MALOUTER", nuance="Cu", Rpe=0, ElectricalConductivity=58.0e+6)
            
            m2 = create_msite(session=session, name="M20022001", conffile="MAGFILEM20022001b.conf", status="On")
            # meme chose que Helices de m1 sauf pour la derniere
            # add Bitters to m2

            m3 = create_msite(session=session, name="M21071901", conffile="MAGFILE2021.07.19.conf", status="On")
            # add Bitters to m2
        
    if args.displaymagnet:
        with Session(engine) as session:
            # TODO get magnet_id by name
            results = query_magnet(session, args.displaymagnet)
            if not results:
                print("cannot find magnet %s" % args.displaymagnet)
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
            for stype in ["Helix", "Ring", "Lead"]:
                mdata[stype]=[]
                objects = get_mparts_type(session=session, magnet_id=magnet.id, type=stype)
                for h in objects:
                    # get material from material_id
                    material = session.get(Material, h.material_id)
                    material_data = material.dict()
                    # remove uneeded stuff
                    for key in ['furnisher', 'ref', 'name', 'id']:
                        material_data.pop(key, None)
                    mdata[stype].append({"geo": h.geom, "material": material_data})
            # print(mdata)
        
        out = open(magnet.name + "-data.json", "x")
        out.write(json.dumps(mdata, indent = 4))
