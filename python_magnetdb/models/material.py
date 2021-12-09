from sqlalchemy import Column, String, Float

from .application_model import ApplicationModel, generate_uuid


class Material(ApplicationModel):
    __tablename__ = "materials"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    t_ref = Column(Float, default=20)
    volumic_mass = Column(Float, default=0)
    specific_heat = Column(Float, default=0)
    alpha = Column(Float, default=0)
    electrical_conductivity = Column(Float)
    thermal_conductivity = Column(Float, default=0)
    magnet_permeability = Column(Float, default=0)
    young = Column(Float, default=0)
    poisson = Column(Float, default=0)
    expansion_coefficient = Column(Float, default=0)
    rpe = Column(Float)
