import os
import tempfile
from argparse import Namespace
from os.path import basename
from traceback import print_exception

from fabric import Connection
from python_magnetsetup.config import appenv
from python_magnetsetup.job import JobManager, JobManagerType
from python_magnetsetup.node import NodeSpec, NodeType
from python_magnetsetup.setup import setup_cmds

from python_magnetdb.models.attachment import Attachment


def run_ssh_simulation(simulation, server):
    simulation.status = "in_progress"
    simulation.save()

    with tempfile.TemporaryDirectory() as local_tempdir:
        ssh_key = f"{local_tempdir}/ssh_key"
        with open(ssh_key, "w") as f:
            f.write(server.private_key)
        connection = Connection(host=server.host, user=server.username, connect_kwargs={
            'key_filename': ssh_key
        })
        current_dir = os.getcwd()
        os.chdir(local_tempdir)

        try:
            print("Downloading setup archive...")
            simulation.setup_output_attachment.download(f"{local_tempdir}/setup.tar.gz")
            remote_temp_dir = connection.run('mktemp -d').stdout.strip()
            connection.put(f"{local_tempdir}/setup.tar.gz", remote_temp_dir)
            print("Extracting setup archive...")
            connection.run(f"tar xvf {remote_temp_dir}/setup.tar.gz -C {remote_temp_dir}")
            print("Generating commands...")
            data_dir = f"{remote_temp_dir}/data"
            args = Namespace(wd=remote_temp_dir,
                             datafile=f"{remote_temp_dir}/config.json",
                             method=simulation.method,
                             time="static" if simulation.static else "transient",
                             geom=simulation.geometry,
                             model=simulation.model,
                             nonlinear=simulation.non_linear,
                             cooling=simulation.cooling,
                             flow_params=f"{remote_temp_dir}/flow_params.json",
                             debug=False,
                             verbose=False,
                             skip_archive=True)
            env = appenv(envfile=None, url_api=data_dir, yaml_repo=f"{remote_temp_dir}/geometries", cad_repo=f"{remote_temp_dir}/cad",
                         mesh_repo=data_dir, simage_repo=server.image_directory, mrecord_repo=data_dir, optim_repo=data_dir)
            node_spec = NodeSpec(name="local-node", otype=NodeType.compute, smp=True, dns="localhost", cores=8,
                                 multithreading=True, manager=JobManager(otype=JobManagerType.none, queues=[]),
                                 mgkeydir=None)
            cmds = setup_cmds(env, args, node_spec, simulation.setup_state['yamlfile'],
                              simulation.setup_state['cfgfile'], simulation.setup_state['xaofile'],
                              simulation.setup_state['meshfile'], remote_temp_dir)

            with connection.cd(remote_temp_dir):
                for (key, value) in cmds.items():
                    if key in ['Unpack', 'Pre', 'Workflow']:
                        continue
                    print(f"Performing {key}...")
                    if key in ['Update_cfg', 'Update_Mesh']:
                        print(value)
                        connection.run(value)
                    else:
                        print(f"bash -c '{cmds['Pre']} && {value}'")
                        connection.run(f"bash -c '{cmds['Pre']} && {value}'")

                print("Archiving results...")
                simulation_name = os.path.basename(os.path.splitext(simulation.setup_state['cfgfile'])[0])
                remote_output_archive = f"{remote_temp_dir}/{simulation_name}.tar.gz"
                connection.run(f"tar cvzf {remote_output_archive} *")
                local_output_archive = f"{local_tempdir}/{simulation_name}.tar.gz"
                connection.get(remote_output_archive, local_output_archive)
                attachment = Attachment.raw_upload(basename(local_output_archive), "application/x-tar", local_output_archive)
                simulation.output_attachment().associate(attachment)

            print("Done!")
            simulation.status = "done"
        except Exception as e:
            simulation.status = "failed"
            print_exception(e)
        os.chdir(current_dir)
        simulation.save()

