"""
Check for unit consistency
Depending on Length base unit
"""

import warnings
from typing import List, Union

from pint import UnitRegistry, Quantity

# Ignore warning for pint
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    Quantity([])

# Pint configuration
ureg = UnitRegistry()
ureg.default_system = 'SI'
ureg.autoconvert_offset_to_baseunit = True


def load_units(distance_unit: str):
    """
    returns units dict
    """

    # units: dict( Quantity: [ in_unit, out_unit ]
    units = {
        "VolumicMass": [ureg.kilogram / ureg.meter ** 3, ureg.kilogram / ureg.Unit(distance_unit) ** 3],
        "ThermalConductivity": [ureg.watt / ureg.meter / ureg.kelvin,
                                ureg.watt / ureg.Unit(distance_unit) / ureg.kelvin],
        "ElectricalConductivity": [ureg.siemens / ureg.meter, ureg.siemens / ureg.Unit(distance_unit)],
        "Young": [ureg.kilogram / ureg.meter / ureg.second, ureg.kilogram / ureg.Unit(distance_unit) / ureg.second],
        "Length": [ureg.millimeter, ureg.Unit(distance_unit)],
        "Area": [ureg.millimeter * ureg.millimeter, ureg.Unit(distance_unit) * ureg.Unit(distance_unit)],
        "mu0": [ureg.henry / ureg.meter, ureg.henry / ureg.Unit(distance_unit)],
        "h": [ureg.watt / ureg.meter ** 2 / ureg.kelvin, ureg.watt / ureg.Unit(distance_unit) ** 2 / ureg.kelvin],
        "Flow": [ureg.liter / ureg.second,
                 ureg.Unit(distance_unit) * ureg.Unit(distance_unit) * ureg.Unit(distance_unit) / ureg.second],
        "Current": [ureg.ampere, ureg.ampere],
        "Power": [ureg.watt, ureg.watt],
        "Temperature": [ureg.degK, ureg.degK]
    }

    return units


def convert_data(units: dict, quantity: Union[float, List[float]], qtype: str, debug: bool = False):
    """
    Returns quantity unit consistant with length unit
    """

    data = None
    if isinstance(quantity, float):
        data = Quantity(quantity, units[qtype][0]).to(units[qtype][1]).magnitude
        if debug:
            print(qtype, quantity, "data=", data)
    elif isinstance(quantity, list):
        data = Quantity(quantity, units[qtype][0]).to(units[qtype][1]).magnitude.tolist()
    else:
        raise Exception(f"convert_data/quantity: unsupported type {type(quantity)} for {qtype}")

    return data
