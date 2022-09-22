import os
import subprocess
import tempfile
from argparse import Namespace
from os.path import basename

from python_magnetdb.models.attachment import Attachment
from python_magnetsetup.config import appenv
from python_magnetsetup.job import JobManager, JobManagerType
from python_magnetsetup.node import NodeSpec, NodeType
from python_magnetsetup.setup import setup_cmds


def run_simulation(simulation):
    simulation.status = "in_progress"
    simulation.save()

    with tempfile.TemporaryDirectory() as tempdir:
        current_dir = os.getcwd()
        os.chdir(tempdir)

        try:
            print("Downloading setup archive...")
            simulation.setup_output_attachment.download(f"{tempdir}/setup.tar.gz")
            print("Extracting setup archive...")
            subprocess.run([f"tar xvf {tempdir}/setup.tar.gz -C {tempdir}"], shell=True)
            print("Generating commands...")
            data_dir = f"{tempdir}/data"
            args = Namespace(wd=tempdir,
                             datafile=f"{tempdir}/config.json",
                             method=simulation.method,
                             time="static" if simulation.static else "transient",
                             geom=simulation.geometry,
                             model=simulation.model,
                             nonlinear=simulation.non_linear,
                             cooling=simulation.cooling,
                             flow_params=f"{tempdir}/flow_params.json",
                             debug=False,
                             verbose=False,
                             skip_archive=True)
            env = appenv(envfile=None, url_api=data_dir, yaml_repo=f"{data_dir}/geometries", cad_repo=f"{data_dir}/cad",
                         mesh_repo=data_dir, simage_repo=os.getenv('IMAGES_DIR'), mrecord_repo=data_dir, optim_repo=data_dir)
            node_spec = NodeSpec(name="local-node", otype=NodeType.compute, smp=True, dns="localhost", cores=8,
                                 multithreading=True, manager=JobManager(otype=JobManagerType.none, queues=[]),
                                 mgkeydir=None)
            cmds = setup_cmds(env, args, node_spec, simulation.setup_state['yamlfile'],
                              simulation.setup_state['cfgfile'], simulation.setup_state['xaofile'],
                              simulation.setup_state['meshfile'], tempdir)

            for (key, value) in cmds.items():
                if key in ['Unpack', 'Pre']:
                    continue
                print(f"Performing {key}...")
                if key in ['Update_cfg', 'Update_Mesh']:
                    print(value)
                    subprocess.run([value], shell=True)
                else:
                    print(f"bash -c '{cmds['Pre']} && {value}'")
                    subprocess.run([f"bash -c \"{cmds['Pre']} && {value}\""], shell=True)

            print("Archiving results...")
            simulation_name = os.path.basename(os.path.splitext(simulation.setup_state['cfgfile'])[0])
            output_archive = f"{tempdir}/{simulation_name}.tar.gz"
            subprocess.run([f"tar cvzf {output_archive} *"], shell=True)
            attachment = Attachment.raw_upload(basename(output_archive), "application/x-tar", output_archive)
            simulation.output_attachment().associate(attachment)
            print("Done!")
            simulation.status = "done"
        except Exception as e:
            simulation.status = "failed"
            raise e
        os.chdir(current_dir)
        simulation.save()
