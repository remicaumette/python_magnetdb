import os

from .config import load_internal_config


def generate_commands(MyEnv, args, name, cfgfile, jsonfile, xaofile, meshfile):
    """
    create cmds

    Watchout: gsmh/salome base mesh is always in millimeter
    For simulation it is madatory to use a mesh in meter except maybe for HDG
    """

    # loadconfig
    AppCfg = load_internal_config()

    # Get current dir
    cwd = os.getcwd()
    if args.wd:
        os.chdir(args.wd)

    # get server from MyEnv,
    # get NP from server (with an heuristic from meshsize)
    # TODO adapt NP to the size of the problem
    # if server is SMP mpirun outside otherwise inside singularity
    from .machines import load_machines

    machines = load_machines()
    if args.debug:
        print(f"machine={MyEnv.compute_server} type={type(MyEnv.compute_server)}")
    server = machines[MyEnv.compute_server]
    NP = server.cores
    if server.multithreading:
        NP = int(NP/2)
    if args.debug:
        print(f"NP={NP} {type(NP)}")

    simage_path = MyEnv.simage_path()
    hifimagnet = AppCfg["mesh"]["hifimagnet"]
    salome = AppCfg["mesh"]["salome"]
    feelpp = AppCfg[args.method]["feelpp"]
    partitioner = AppCfg["mesh"]["partitioner"]
    if "exec" in AppCfg[args.method]:
        exec = AppCfg[args.method]["exec"]
    if "exec" in AppCfg[args.method][args.time][args.geom][args.model]:
        exec = AppCfg[args.method][args.time][args.geom][args.model]
    pyfeel = ' -m workflows.cli' # commisioning, fixcooling

    if "mqs" in args.model or "mag" in args.model:
        geocmd = f"salome -w1 -t $HIFIMAGNET/HIFIMAGNET_Cmd.py args:{name},--air,2,2,--wd,data/geometries"
        meshcmd = f"salome -w1 -t $HIFIMAGNET/HIFIMAGNET_Cmd.py args:{name},--air,2,2,--wd,$PWD,mesh,--group,CoolingChannels,Isolants"
    else:
        geocmd = f"salome -w1 -t $HIFIMAGNET/HIFIMAGNET_Cmd.py args:{name},2,2,--wd,data/geometries"
        meshcmd = f"salome -w1 -t $HIFIMAGNET/HIFIMAGNET_Cmd.py args:{name},2,2,--wd,$PWD,mesh,--group,CoolingChannels,Isolants"

    gmshfile = meshfile.replace(".med", ".msh")
    meshconvert = ""

    if args.geom == "Axi" and args.method == "cfpdes" :
        if "mqs" in args.model or "mag" in args.model:
            geocmd = f"salome -w1 -t $HIFIMAGNET/HIFIMAGNET_Cmd.py args:{name},--axi,--air,2,2,--wd,data/geometries"
        else:
            geocmd = f"salome -w1 -t $HIFIMAGNET/HIFIMAGNET_Cmd.py args:{name},--axi,--wd,data/geometries"

        # if gmsh:
        meshcmd = f"python3 -m python_magnetgeo.xao {xaofile} --wd data/geometries mesh --group CoolingChannels --geo {name} --lc=1"
    else:
        gmshfile = meshfile.replace(".med", ".msh")
        meshconvert = f"gmsh -0 {meshfile} -bin -o {gmshfile}"

    scale = ""
    if args.method != "HDG":
        scale = "--mesh.scale=0.001"
    h5file = xaofile.replace(".xao", "_p.json")
    partcmd = f"{partitioner} --ifile {gmshfile} --ofile {h5file} --part {NP} {scale}"

    tarfile = cfgfile.replace("cfg", "tgz")
    # TODO if cad exist do not print CAD command
    cmds = {
        "Pre": f"export HIFIMAGNET={hifimagnet}",
        "Unpack": f"tar zxvf {tarfile}",
        "CAD": f"singularity exec {simage_path}/{salome} {geocmd}"
    }

    # TODO add mount point for MeshGems if 3D otherwise use gmsh for Axi
    # to be changed in the future by using an entry from magnetsetup.conf MeshGems or gmsh
    MeshGems_licdir = server.mgkeydir
    cmds["Mesh"] = f"singularity exec -B {MeshGems_licdir}:/opt/DISTENE/license:ro {simage_path}/{salome} {meshcmd}"
    # if gmsh:
    #    cmds["Mesh"] = f"singularity exec -B /opt/MeshGems:/opt/DISTENE/license:ro {simage_path}/{salome} {meshcmd}"

    if meshconvert:
        cmds["Convert"] = f"singularity exec {simage_path}/{salome} {meshconvert}"

    if args.geom == "3D":
        cmds["Partition"] = f"singularity exec {simage_path}/{feelpp} {partcmd}"
        meshfile = h5file
        update_partition = f"perl -pi -e \'s|gmsh.partition=.*|gmsh.partition = 0|\' {cfgfile}"

    # TODO add command to change mesh.filename in cfgfile
    update_cfgmesh = f"perl -pi -e \'s|mesh.filename=.*|mesh.filename=\$cfgdir/data/geometries/{meshfile}|\' {cfgfile}"
    if args.geom =="Axi":
        update_cfg = f"perl -pi -e 's|# mesh.scale =|mesh.scale =|' {cfgfile}"
        cmds["Update_cfg"] = update_cfg

    cmds["Update_Mesh"] = update_cfgmesh
    if args.geom == "3D":
        cmds["Update_Partition"] = update_partition

    if server.smp:
        feelcmd = f"{exec} --config-file {cfgfile}"
        pyfeelcmd = f"python {pyfeel}"
        cmds["Run"] = f"mpirun -np {NP} singularity exec {simage_path}/{feelpp} {feelcmd}"
        cmds["Workflow"] = f"mpirun -np {NP} singularity exec {simage_path}/{feelpp} {pyfeelcmd} {cfgfile}"

    else:
        feelcmd = f"mpirun -np {NP} {exec} --config-file {cfgfile}"
        pyfeelcmd = f"mpirun -np {NP} python {pyfeel} {cfgfile}"
        cmds["Run"] = f"singularity exec {simage_path}/{feelpp} {feelcmd}"
        cmds["Workflow"] = f"singularity exec {simage_path}/{feelpp} {pyfeelcmd}"

    # TODO jobmanager if server.manager != JobManagerType.none
    # Need user email at this point
    # Template for oar and slurm

    # TODO what about postprocess??

    return cmds
