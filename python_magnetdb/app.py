from typing import List, Optional

from sqlmodel import Session, select

from .database import create_db_and_tables, engine
from .models import MPart, Magnet, MSite, MRecord
from .models import MaterialBase, Material, MaterialCreate, MaterialRead


def create_mparts():
    with Session(engine) as session:
        m1 = MSite(name="M1", conffile="M1.coffile", status="On")
        session.add(m1)
        m2 = MSite(name="M2", conffile="M1.coffile", status="On")
        session.add(m2)
        session.commit()

        HL31 = Magnet(name="HL-31", be="M12_XYZ", geom="HL-31.yml", status="On", msites=[m1])
        HL34 = Magnet(name="HL-34", be="M21_XYZ", geom="HL-34.yml", status="Off", msites=[m2])
        session.add(HL31)
        session.add(HL34)

        bitter = Magnet(name="Bext", be="M45_XYZ", geom="Bitter.yml", status="On", msites=[m1])
        session.add(bitter)
        session.commit()

        cu5ag = Material(name="Cu5Ag", Tref=20, VolumicMass=10, SpecificHeat=20, ElectricalConductivity=56.0e+6, ThermalConductivity=380, MagnetPermeability=1, Young=120e+6, Poisson=0.3, CoefDilatation=0.016)
        session.add(cu5ag)
        cu = Material(name="Cu", Tref=20, VolumicMass=10, SpecificHeat=20, ElectricalConductivity=58.0e+6, ThermalConductivity=400, MagnetPermeability=1, Young=120e+6, Poisson=0.3, CoefDilatation=0.016)
        session.add(cu)
        session.commit()

        helix = MPart(name="H1", type="Helix", be="REFCATIA", geom="H1.yml", status="On", material_id=cu5ag.id, magnets=[HL31])
        session.add(helix)
        
        h2 =  MPart(name="H2", type="Helix", be="REFCATIA", geom="H2.yml", status="On", material_id=cu5ag.id, magnets=[HL31, HL34])
        session.add(h2)
        
        B1 =  MPart(name="B1", type="Bitter", be="REFCATIA", geom="B1.yml", status="On", material_id=cu.id, magnets=[bitter])
        session.add(B1)
        B2 =  MPart(name="B2", type="Bitter", be="REFCATIA", geom="B2.yml", status="On", material_id=cu.id, magnets=[bitter])
        session.add(B2)
        
        session.commit()

        session.refresh(m1)
        session.refresh(m2)
        session.refresh(HL31)
        session.refresh(HL34)
        session.refresh(bitter)
        session.refresh(cu5ag)
        session.refresh(cu)
        session.refresh(helix)
        session.refresh(h2)
        session.refresh(B1)
        session.refresh(B2)

        print("Created Material:", cu5ag)
        print("Created MPart:", helix)
        print("Created Magnet:", HL31)

def main():
    create_db_and_tables()
    create_mparts()

if __name__ == "__main__":
    main()