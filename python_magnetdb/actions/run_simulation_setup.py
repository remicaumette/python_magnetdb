import json
import os
import tempfile
from argparse import Namespace
from os.path import basename

from python_magnetdb.models.attachment import Attachment
from python_magnetdb.models.magnet import Magnet
from python_magnetdb.models.material import Material
from python_magnetsetup.config import appenv
from python_magnetsetup.setup import setup


def generate_magnet_config(magnet, directory):
    magnet = Magnet\
        .with_('magnet_parts.part.geometry', 'magnet_parts.part.material', 'site_magnets.site', 'cao', 'geometry') \
        .find(magnet.id)

    def format_material(material):
        return {
            "Tref": material.t_ref,
            "VolumicMass": material.volumic_mass,
            "alpha": material.alpha,
            "ElectricalConductivity": material.electrical_conductivity,
            "MagnetPermeability": material.magnet_permeability,
            "Poisson": material.poisson,
            "Rpe": material.rpe,
            "SpecificHeat": material.specific_heat,
            "ThermalConductivity": material.thermal_conductivity,
            "Young": material.young,
            "CoefDilatation": material.expansion_coefficient,
            "nuance": material.nuance
        }

    magnet.geometry.download(f"{directory}/data/{magnet.geometry.filename}")
    payload = {'geom': magnet.geometry.filename}
    insulator_payload = format_material(Material.where('name', 'MAT_ISOLANT').first())

    for magnet_part in magnet.magnet_parts:
        if not magnet_part.active:
            continue

        if magnet_part.part.type.capitalize() not in payload:
            payload[magnet_part.part.type.capitalize()] = []
        magnet_part.part.geometry.download(f"{directory}/data/{magnet_part.part.geometry.filename}")
        payload[magnet_part.part.type.capitalize()].append({
            'geom': magnet_part.part.geometry.filename,
            'material': format_material(magnet_part.part.material),
            'insulator': insulator_payload
        })

    with open(f"{directory}/config.json", "w+") as file:
        file.write(json.dumps(payload))


def generate_config(simulation, directory):
    os.mkdir(f"{directory}/data")
    generate_magnet_config(simulation.resource, directory)


def run_simulation_setup(simulation):
    simulation.status = "setup_in_progress"
    simulation.save()
    with tempfile.TemporaryDirectory() as tempdir:
        print(f"generating config in {tempdir}...")
        generate_config(simulation, tempdir)
        print("generating config done")
        print("running setup...")
        data_dir = f"{tempdir}/data"
        args = Namespace(wd=tempdir,
                         datafile=f"{tempdir}/config.json",
                         method=simulation.method,
                         time="static" if simulation.static else "transient",
                         geom=simulation.geometry,
                         model=simulation.model,
                         nonlinear=simulation.non_linear,
                         cooling=simulation.cooling,
                         flow_params=f"{os.getcwd()}/flow_params.json",
                         debug=False,
                         verbose=False)

        # todo: envfile=None
        env = appenv(url_api=data_dir, yaml_repo=data_dir, cad_repo=data_dir, mesh_repo=data_dir,
                     simage_repo=data_dir, mrecord_repo=data_dir, optim_repo=data_dir)
        with open(f"{tempdir}/config.json", "r") as config_file:
            config = json.load(config_file)
            (name, cfgfile, jsonfile, xaofile, meshfile, tarfile) = setup(env, args, config, f"{tempdir}/{simulation.resource.name}")
            attachment = Attachment.raw_upload(basename(tarfile), "application/x-tar", tarfile)
            simulation.result().associate(attachment)
            simulation.status = "done"
            simulation.save()
