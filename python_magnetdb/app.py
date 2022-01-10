import json
from math import nan

from .checks import *
from .crud import *
from .database import perform_migrations, engine
from .operations import *


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
    perform_migrations()

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

IACS = 58.e+6

# TODO: create a clip.py

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--createdb", help="createdb", action='store_true')
    parser.add_argument("--migrate", help="migrate db", action='store_true')
    parser.add_argument("--createsite", help="createsite", action='store_true')
    parser.add_argument("--displaymagnet", help="display magnet", type=str, default=None)
    parser.add_argument("--displaymsite", help="display msite", type=str, default=None)
    parser.add_argument("--checkmaterial", help="check material data", action='store_true')
    args = parser.parse_args()

    if args.createdb:
        main()

    if args.migrate:
        perform_migrations()

    if args.createsite:
        with Session(engine) as session:
            # Test
            # Insert Two Helices
            m1 = create_msite(session=session, name="MTest", conffile="MAGFILE2019.06.20.35T.conf", status=MStatus.defunct)

            Helices = create_magnet(session=session, name="HL-test", be="HL-34-001-A", geom="test.yaml", status=MStatus.operation, msites=[m1])

            MAT_TEST1 = create_material(session=session, name="MAT_TEST1", nuance="Cu5Ag5,08",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=380, alpha=3.6e-3, ElectricalConductivity=50.1e+6,
                                    ThermalConductivity=360, MagnetPermeability=1, Young=127e+9, Poisson=0.335,  CoefDilatation=18e-6,
                                    Rpe=481000000.0)

            create_mpart(session=session, name='HL-34_H1', mtype='Helix', be='HL-34-001-A', geom='HL-31_H1.yaml', status=MStatus.operation, magnets=[Helices], material=MAT_TEST1)
            create_mpart(session=session, name='HL-34_H2', mtype='Helix', be='HL-34-001-A', geom='HL-31_H2.yaml', status=MStatus.operation, magnets=[Helices], material=MAT_TEST1)

            MAT_TEST2 = create_material(session=session, name="MAT_TEST2", nuance="Cu5Ag5,08",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=380, alpha=3.6e-3, ElectricalConductivity=50.1e+6,
                                    ThermalConductivity=360, MagnetPermeability=1, Young=127e+9, Poisson=0.335,  CoefDilatation=18e-6,
                                    Rpe=481000000.0)
            create_mpart(session=session, name="Ring-H1H2", mtype='Ring', be="HL-34-001-A", geom='Ring-H1H2.yaml', status=MStatus.operation, magnets=[Helices], material=MAT_TEST2)
            ####################

            ####################
            # M19061901
            ####################

            # Definition of Site
            m2 = create_msite(session=session, name="M10", conffile="MAGFILE2019.06.20.35T.conf", status=MStatus.operation)

            # Definition of M19061901 magnet
            M19061901 = create_magnet(session=session, name="M19061901", be="unknow", geom="HL-31.yaml", status=MStatus.operation, msites=[m2])
            Bitters = create_magnet(session=session, name="M9Bitters", be="B_XYZ", geom="M9Bitters.yaml", status=MStatus.operation, msites=[m2])
            CuAg01 = create_material(session=session, name="B_CuAg01", nuance="CuAg01",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=380, alpha=3.6e-3, ElectricalConductivity=50.1e+6,
                                    ThermalConductivity=360, MagnetPermeability=1, Young=127e+9, Poisson=0.335,  CoefDilatation=18e-6,
                                    Rpe=481000000.0)
            create_mpart(session=session, name='M9Bi', mtype='Bitter', be='BI-03-002-A', geom='M9Bitters_Bi.yaml', status=MStatus.operation, magnets=[Bitters], material=CuAg01)
            create_mpart(session=session, name='M9Be', mtype='Bitter', be='BE-03-002-A', geom='M9Bitters_Be.yaml', status=MStatus.operation, magnets=[Bitters], material=CuAg01)

            m1 = create_msite(session=session, name="MTest2", conffile="MAGFILE2019.06.20.35T.conf", status=MStatus.defunct)
            msite_add_magnet(session=session, msite=m1, magnet=Helices)
            msite_add_magnet(session=session, msite=m1, magnet=Bitters)


    if args.displaymagnet:
        with Session(engine) as session:
            mdata = get_magnet_data(session, args.displaymagnet)
            with open(args.displaymagnet + "-data.json", "x") as out:
                out.write(json.dumps(mdata, indent = 4))

    if args.displaymsite:
        import yaml
        with Session(engine) as session:
            mdata = get_msite_data(session, args.displaymsite)
            with open(args.displaymsite + "-data.yaml", "x") as out:
                out.write("!<MSite>\n")
                yaml.dump(mdata, out)



    if args.checkmaterial:
        with Session(engine) as session:
            statement = select(Material)
            materials = session.exec(statement).all()
            print("\n=== Checking material data consistency ===")
            for material in materials:
                undef_set = check_material(session, material.id)
                if undef_set:
                    print(material.name, ":", check_material(session, material.id))

