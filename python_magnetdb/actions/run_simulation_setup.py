import json
import os
import subprocess
import tempfile
from argparse import Namespace
from os.path import basename

from python_magnetdb.actions.generate_simulation_config import generate_simulation_config
from python_magnetdb.models.attachment import Attachment
from python_magnetdb.models.magnet import Magnet
from python_magnetsetup.config import appenv
from python_magnetsetup.setup import setup


def prepare_directory(simulation, directory):
    magnet = Magnet.with_('magnet_parts.part.geometry', 'magnet_parts.part.cad_attachments', 'geometry',
                          'magnet_parts.part.material', 'site_magnets.site', 'cad_attachments').find(simulation.resource_id)
    os.mkdir(f"{directory}/data")
    os.mkdir(f"{directory}/data/geometries")
    os.mkdir(f"{directory}/data/cad")
    if magnet.geometry:
        magnet.geometry.download(f"{directory}/data/geometries/{magnet.geometry.filename}")
    if magnet.cad_attachments:
        for cad_attachment in magnet.cad_attachments:
            cad_attachment.download(f"{directory}/data/cad/{cad_attachment.filename}")
    for magnet_part in magnet.magnet_parts:
        if not magnet_part.active:
            continue
        if magnet_part.part.geometry:
            magnet_part.part.geometry.download(f"{directory}/data/geometries/{magnet_part.part.geometry.filename}")
        if magnet_part.part.cad_attachments:
            for cad_attachment in magnet_part.part.cad_attachments:
                cad_attachment.download(f"{directory}/data/cad/{cad_attachment.filename}")
    with open(f"{directory}/config.json", "w+") as file:
        file.write(json.dumps(generate_simulation_config(simulation)))


def run_simulation_setup(simulation):
    simulation.status = "setup_in_progress"
    simulation.save()
    with tempfile.TemporaryDirectory() as tempdir:
        print(f"generating config in {tempdir}...")
        prepare_directory(simulation, tempdir)
        print("generating config done")
        print("running setup...")
        subprocess.run([f"ls -lR {tempdir}"], shell=True)
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
        env = appenv(envfile=None, url_api=data_dir, yaml_repo=f"{data_dir}/geometries", cad_repo=f"{data_dir}/cad",
                     mesh_repo=data_dir, simage_repo=data_dir, mrecord_repo=data_dir, optim_repo=data_dir)
        current_dir = os.getcwd()
        try:
            with open(f"{tempdir}/config.json", "r") as config_file:
                config = json.load(config_file)
                (name, cfgfile, jsonfile, xaofile, meshfile, tarfile) = setup(env, args, config, f"{tempdir}/{simulation.resource.name}")
                attachment = Attachment.raw_upload(basename(tarfile), "application/x-tar", tarfile)
                simulation.result().associate(attachment)
                simulation.status = "done"
        except Exception as e:
            raise e
            simulation.status = "failed"
        os.chdir(current_dir)
        simulation.save()
