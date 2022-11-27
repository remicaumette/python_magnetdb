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


def run_cmd(connection, cmd, stdout):
    res = connection.run(cmd)
    stdout.write(f"=== RUNNING CMD: {cmd}\n")
    stdout.write(f"===\n")
    stdout.write(res.stdout)
    if len(res.stderr) > 0:
        stdout.write(f"=== STDERR:\n")
        stdout.write(f"===\n")
        stdout.write(res.stderr)
    stdout.write(f"=== STATUS CODE: {res.exited}\n")
    return res.stdout


def run_ssh_simulation(simulation, server):
    simulation.status = "in_progress"
    simulation.save()

    with tempfile.TemporaryDirectory() as local_tempdir:
        current_dir = os.getcwd()
        os.chdir(local_tempdir)
        log_file_path = f"{local_tempdir}/debug.log"
        with open(log_file_path, "a") as log_file:
            try:
                ssh_key = f"{local_tempdir}/ssh_key"
                with open(ssh_key, "w") as f:
                    f.write(server.private_key)
                connection = Connection(host=server.host, user=server.username, connect_kwargs={
                    'key_filename': ssh_key
                })


                log_file.write("Downloading setup archive...\n")
                simulation.setup_output_attachment.download(f"{local_tempdir}/setup.tar.gz")
                remote_temp_dir = run_cmd(connection, 'mktemp -d', log_file).strip()
                connection.put(f"{local_tempdir}/setup.tar.gz", remote_temp_dir)
                log_file.write("Extracting setup archive...\n")
                run_cmd(connection, f"tar xvf {remote_temp_dir}/setup.tar.gz -C {remote_temp_dir}", log_file)
                log_file.write("Generating commands...\n")
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
                                 np=0,
                                 debug=False,
                                 verbose=False,
                                 skip_archive=True)
                env = appenv(envfile=None, url_api=data_dir, yaml_repo=f"{remote_temp_dir}/geometries",
                             cad_repo=f"{remote_temp_dir}/cad", mesh_repo=data_dir, simage_repo=server.image_directory,
                             mrecord_repo=data_dir, optim_repo=data_dir)
                node_spec = NodeSpec(name="local-node", otype=NodeType.compute, smp=True, dns="localhost", cores=8,
                                     multithreading=True, manager=JobManager(otype=JobManagerType.none, queues=[]),
                                     mgkeydir=None)
                cmds = setup_cmds(env, args, node_spec, simulation.setup_state['yamlfile'],
                                  simulation.setup_state['cfgfile'], simulation.setup_state['xaofile'],
                                  simulation.setup_state['meshfile'], remote_temp_dir)

                # Save cmds in a file
                with open("cmds.txt", "a") as f:
                    log_file.write("Saving commands...\n")
                    for (key, value) in cmds.items():
                        f.write(f'{key}: {value}')

                with connection.cd(remote_temp_dir):
                    for (key, value) in cmds.items():
                        if key in ['Unpack', 'Workflow']:
                            continue
                        log_file.write(f"Performing {key}...\n")
                        if key in ['Update_cfg', 'Update_Mesh']:
                            run_cmd(connection, value, log_file)
                        else:
                            run_cmd(connection, f"bash -c '{value}'", log_file)

                    log_file.write("Archiving results...\n")
                    simulation_name = os.path.basename(os.path.splitext(simulation.setup_state['cfgfile'])[0])
                    remote_output_archive = f"{remote_temp_dir}/{simulation_name}.tar.gz"
                    run_cmd(connection, f"tar cvzf {remote_output_archive} *", log_file)
                    local_output_archive = f"{local_tempdir}/{simulation_name}.tar.gz"
                    connection.get(remote_output_archive, local_output_archive)
                    simulation.output_attachment().associate(
                        Attachment.raw_upload(basename(local_output_archive), "application/x-tar", local_output_archive)
                    )
                log_file.write("Done!\n")
                simulation.status = "done"
            except Exception as e:
                simulation.status = "failed"
                print_exception(e)
            simulation.log_attachment().associate(Attachment.raw_upload("debug.log", "text/plain", log_file_path))
            os.chdir(current_dir)
            simulation.save()
