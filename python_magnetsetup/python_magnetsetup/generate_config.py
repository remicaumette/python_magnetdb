"""
Create template json model files for Feelpp/HiFiMagnet simu
From a yaml definition file of an insert

Inputs:
* method : method of solve, with feelpp cfpdes, getdp...
* time: stationnary or transient case
* geom: geometry of solve, 3D or Axi
* model: physic solved, thermic, thermomagnetism, thermomagnetism-elastic
* phytype: if the materials are linear or non-linear
* cooling: what type of cooling, mean or grad

Output:
* tmp.json

App setup is stored in a json file that defines
the mustache template to be used.

Default path:
magnetsetup.json
mustache templates
"""

# TODO check for unit consistency
# depending on Length base unit

import os
import tarfile
from typing import List

import yaml

from python_magnetgeo import Bitter, Supra
from .bitter import Bitter_setup
from .cfg import create_cfg
from .config import load_internal_config, appenv, check_templates
from .file_utils import MyOpen, findfile, search_paths
from .insert import Insert_setup, Insert_simfile
from .jsonmodel import create_json
from .objects import load_object_from_api, load_attachment
from .supra import Supra_setup, Supra_simfile
from .utils import NMerge


def magnet_simfile(MyEnv, confdata: str, addAir: bool = False):
    """
    """
    files = []
    yaml_file = confdata["geom"]

    if "Helix" in confdata:
        print("Load an insert")
        attachment = load_attachment(confdata["geom"])
        cad = yaml.load(attachment.data, Loader=yaml.FullLoader)
        files.append(attachment.name)
        for tmp_f in Insert_simfile(MyEnv, confdata, cad, addAir):
            files.append(tmp_f)
        return files

    for magnet_type in ["Bitter", "Supra"]:
        if magnet_type not in confdata:
            continue

        print(f"load a {magnet_type} insert")
        try:
            with MyOpen(yaml_file, 'r', paths=search_paths(MyEnv, "geom")) as cfgdata:
                cad = yaml.load(cfgdata, Loader = yaml.FullLoader)
                files.append(cfgdata.name)
        except:
            pass

        # loop on mtype
        for obj in confdata[magnet_type]:
            print("obj:", obj)
            cad = None
            yaml_file = obj["geom"]
            with MyOpen(yaml_file, 'r', paths=search_paths(MyEnv, "geom")) as cfgdata:
                cad = yaml.load(cfgdata, Loader = yaml.FullLoader)

            if isinstance(cad, Bitter.Bitter):
                files.append(cfgdata.name)
            elif isinstance(cad, Supra):
                files.append(cfgdata.name)
                struct = Supra_simfile(MyEnv, obj, cad)
                if struct:
                    files.append(struct)
            else:
                raise Exception(f"setup: unexpected cad type {type(cad)}")

    return files

def magnet_setup(MyEnv, confdata: str, method_data: List, templates: dict, debug: bool=False):
    """
    Creating dict for setup for magnet
    """

    print("magnet_setup")
    if debug:
        print(f"magnet_setup: confdata: {confdata}"),

    mdict = {}
    mmat = {}
    mpost = {}

    if "Helix" in confdata:
        print("Load an insert")
        attachment = load_attachment(confdata["geom"])
        cad = yaml.load(attachment, Loader=yaml.FullLoader)
        (mdict, mmat, mpost) = Insert_setup(MyEnv, confdata, cad, method_data, templates, debug)

    for mtype in ["Bitter", "Supra"]:
        if mtype in confdata:
            # TODO check case with only 1 Bitter???

            # loop on mtype
            for obj in confdata[mtype]:
                if debug: print("obj:", obj)
                yamlfile = obj["geom"]
                cad = None
                with MyOpen(yamlfile, 'r', paths=search_paths(MyEnv, "geom")) as cfgdata:
                    cad = yaml.load(cfgdata, Loader = yaml.FullLoader)
                print(f"load a {mtype} insert: {cad.name} ****")

                if isinstance(cad, Bitter.Bitter):
                    (tdict, tmat, tpost) = Bitter_setup(MyEnv, obj, cad, method_data, templates, debug)
                    # print("Bitter tpost:", tpost)
                elif isinstance(cad, Supra):
                    (tdict, tmat, tpost) = Supra_setup(MyEnv, obj, cad, method_data, templates, debug)
                else:
                    raise Exception(f"setup: unexpected cad type {str(type(cad))}")

                if debug: print("tdict:", tdict)
                mdict = NMerge(tdict, mdict, debug, "magnet_setup Bitter/Supra mdict")

                if debug: print("tmat:", tmat)
                mmat = NMerge(tmat, mmat, debug, "magnet_setup Bitter/Supra mmat")

                if debug: print("tpost:", tpost)
                # print(f"magnet_setup {cad.name}: tpost[current_H]={tpost['current_H']}")
                mpost = NMerge(tpost, mpost, debug, "magnet_setup Bitter/Supra mpost") # debug)
                # print(f"magnet_setup {cad.name}: mpost[current_H]={mpost['current_H']}")

    if debug:
        print("magnet_setup: mdict=", mdict)
    return (mdict, mmat, mpost)

def msite_simfile(MyEnv, confdata: str, session=None, addAir: bool = False):
    """
    Creating list of simulation files for msite
    """

    files = []

    # TODO: get xao and brep if they exist, otherwise go on
    # TODO: add suffix _Air if needed ??
    try:
        xaofile = confdata["name"] + ".xao"
        if addAir:
            xaofile = confdata["name"] + "_withAir.xao"
        f =findfile(xaofile, paths=search_paths(MyEnv, "cad"))
        files.append(f)

        brepfile = confdata["name"] + ".brep"
        if addAir:
            brepfile = confdata["name"] + "_withAir.brep"
        f = findfile(brepfile, paths=search_paths(MyEnv, "cad"))
        files.append(f)
    except:
        for magnet in confdata["magnets"]:
            try:
                mconfdata = load_object_from_api("magnets", magnet)
            except:
                raise Exception(f"msite_simfile: failed to load {magnet} from magnetdb")

            files += magnet_simfile(MyEnv, mconfdata)

    return files

def msite_setup(MyEnv, confdata: str, method_data: List, templates: dict, debug: bool=False, session=None):
    """
    Creating dict for setup for msite
    """
    print("msite_setup:", "debug=", debug)
    print("msite_setup:", "confdata=", confdata)
    print("msite_setup: confdata[magnets]=", confdata["magnets"])

    mdict = {}
    mmat = {}
    mpost = {}

    for magnet in confdata["magnets"]:
        print(f"magnet:  {magnet}")
        try:
            mconfdata = load_object_from_api("magnets", magnet)
        except:
            raise Exception(f"setup: failed to load {magnet} from magnetdb")

        if debug:
            print("mconfdata[geom]:", mconfdata["geom"])

        (tdict, tmat, tpost) = magnet_setup(MyEnv, mconfdata, method_data, templates, debug)

        # print("tdict[part_electric]:", tdict['part_electric'])
        # print("tdict[part_thermic]:", tdict['part_thermic'])
        mdict = NMerge(tdict, mdict, debug, "msite_setup/tdict")
        # print("mdict[part_electric]:", mdict['part_electric'])
        # print("mdict[part_thermic]:", mdict['part_thermic'])

        # print("tmat:", tmat)
        mmat = NMerge(tmat, mmat, debug, "msite_setup/tmat")
        # print("NewMerge:", NMerge(tmat, mmat))
        # print("mmat:", mmat)

        # print("tpost:", tpost)
        mpost = NMerge(tpost, mpost, debug, "msite_setup/tpost") #debug)
        # print("NewMerge:", mpost)

    # print("mdict:", mdict)
    return (mdict, mmat, mpost)

def generate_config(MyEnv, args, confdata, jsonfile, session=None):
    """
    """
    print("setup/main")

    # loadconfig
    internal_config = load_internal_config()

    # Get current dir
    cwd = os.getcwd()
    if args.wd:
        os.chdir(args.wd)

    # load appropriate templates
    # TODO force millimeter when args.method == "HDG"
    method_data = [args.method, args.time, args.geom, args.model, args.cooling, "meter"]

    # TODO: if HDG meter -> millimeter
    templates = loadtemplates(MyEnv, internal_config, method_data, (not args.nonlinear))

    mdict = {}
    mmat = {}
    mpost = {}

    if args.debug:
        print("confdata:", confdata)
    cad_basename = ""
    if "geom" in confdata:
        print(f"Load a magnet {jsonfile} ", f"debug: {args.debug}")
        attachment = load_attachment(confdata["geom"])
        cad = yaml.load(attachment, Loader=yaml.FullLoader)
        cad_basename = cad.name

        (mdict, mmat, mpost) = magnet_setup(MyEnv, confdata, method_data, templates, args.debug or args.verbose)
    else:
        print("Load a msite %s" % confdata["name"], "debug:", args.debug)
        # print("confdata:", confdata)
        cad_basename = confdata["name"]

        # why do I need that???
        try:
            findfile(confdata["name"] + ".yaml", search_paths(MyEnv, "geom"))
        except FileNotFoundError as e:
            print("confdata:", confdata)
            print(f"try to create {MyEnv.yaml_repo + '/' + confdata['name'] + '.yaml'}")
            # for obj in confdata[mtype]:
            with open(MyEnv.yaml_repo + '/' + confdata["name"] + ".yaml", "x") as out:
                out.write("!<MSite>\n")
                yaml.dump(confdata, out)
            print(f"try to create {confdata['name']}.yaml done")

        (mdict, mmat, mpost) = msite_setup(MyEnv, confdata, method_data, templates, args.debug or args.verbose, session)
        # print(f"setup: msite mpost={mpost['current_H']}")

    name = jsonfile
    if name in confdata:
        name = confdata["name"]
        print(f"name={name} from confdata")

    # create cfg
    jsonfile += "-" + args.method
    jsonfile += "-" + args.model
    if args.nonlinear:
        jsonfile += "-nonlinear"
    jsonfile += "-" + args.geom
    jsonfile += "-sim.json"
    cfgfile = jsonfile.replace(".json", ".cfg")

    addAir = False
    if 'mag' in args.model or 'mqs' in args.model:
        addAir = True

    # retreive xaofile and meshfile
    xaofile = cad_basename + ".xao"
    if args.geom == "Axi" and args.method == "cfpdes" :
        xaofile = cad_basename + "-Axi.xao"
        if "mqs" in args.model or "mag" in args.model:
            xaofile = cad_basename + "-Axi_withAir.xao"

    meshfile = xaofile.replace(".xao", ".med")
    if args.geom == "Axi" and args.method == "cfpdes" :
        # # if gmsh:
        meshfile = xaofile.replace(".xao", ".msh")
    print(f"setup: meshfile={meshfile}")

    # TODO create_mesh() or load_mesh()
    # generate properly meshfile for cfg
    # generate solver section for cfg
    # here name is from args (aka name of magnet and/or msite if from db)
    create_cfg(cfgfile, name, meshfile, args.nonlinear, jsonfile, templates["cfg"], method_data, args.debug)

    # create json
    create_json(jsonfile, mdict, mmat, mpost, templates, method_data, args.debug)

    # copy some additional json file
    material_generic_def = ["conductor", "insulator"]
    if args.time == "transient":
        material_generic_def.append("conduct-nosource") # only for transient with mqs

    # create list of files to be archived
    sim_files = [cfgfile, jsonfile]
    if args.method == "cfpdes":
        if args.debug: print("cwd=", cwd)
        from shutil import copyfile
        for jfile in material_generic_def:
            filename = internal_config[args.method][args.time][args.geom][args.model]["filename"][jfile]
            src = os.path.join(MyEnv.template_path(), args.method, args.geom, args.model, filename)
            dst = os.path.join(jfile + "-" + args.method + "-" + args.model + "-" + args.geom + ".json")
            if args.debug:
                print(jfile, "filename=", filename, "src=%s" % src, "dst=%s" % dst)
            copyfile(src, dst)
            sim_files.append(dst)

    # list files to be archived

    # actually we dont store mesh files in magnetdb
    # try:
    #     mesh = findfile(meshfile, search_paths(MyEnv, "mesh"))
    #     sim_files.append(mesh)

    if "geom" in confdata:
        print("geo:", name)
        yamlfile = confdata["geom"]
        print(confdata)
        # sim_files += magnet_simfile(MyEnv, confdata, addAir)
    else:
        yamlfile = confdata["name"] + ".yaml"
        # sim_files += msite_simfile(MyEnv, confdata, session, addAir)

    if args.debug:
        print("List of simulations files:", sim_files)
    tarfilename = cfgfile.replace('cfg', 'tgz')
    # if os.path.isfile(os.path.join(cwd, tarfilename)):
    #     os.remove(os.path.join(cwd, tarfilename))
    #
    # tar = tarfile.open(tarfilename, "w:gz")
    # for filename in sim_files:
    #     if args.debug:
    #         print(f"add {filename} to {tarfilename}")
    #     tar.add(filename)
    #     for mname in material_generic_def:
    #         if mname in filename:
    #             if args.debug: print(f"remove {filename}")
    #             os.unlink(filename)
    # tar.add('flow_param.json')
    # tar.close()

    return (yamlfile, cfgfile, jsonfile, xaofile, meshfile, tarfilename)


def loadtemplates(appenv: appenv, appcfg: dict, method_data: List[str], linear: bool = True, debug: bool = False):
    """
    Load templates into a dict

    method_data:
    method
    time
    geom
    model
    cooling

    """

    [method, time, geom, model, cooling, units_def] = method_data
    template_path = os.path.join(appenv.template_path(), method, geom, model)

    cfg_model = appcfg[method][time][geom][model]["cfg"]
    json_model = appcfg[method][time][geom][model]["model"]
    if linear:
        conductor_model = appcfg[method][time][geom][model]["conductor-linear"]
    else:
        if geom == "3D":
            json_model = appcfg[method][time][geom][model]["model-nonlinear"]
        conductor_model = appcfg[method][time][geom][model]["conductor-nonlinear"]
    insulator_model = appcfg[method][time][geom][model]["insulator"]

    fcfg = os.path.join(template_path, cfg_model)
    if debug:
        print("fcfg:", fcfg, type(fcfg))
    fmodel = os.path.join(template_path, json_model)
    fconductor = os.path.join(template_path, conductor_model)
    finsulator = os.path.join(template_path, insulator_model)
    if 'th' in model:
        cooling_model = appcfg[method][time][geom][model]["cooling"][cooling]
        flux_model = appcfg[method][time][geom][model]["cooling-post"][cooling]
        stats_T_model = appcfg[method][time][geom][model]["stats_T"]

        fcooling = os.path.join(template_path, cooling_model)
        frobin = os.path.join(template_path, appcfg[method][time][geom][model]["cooling"]["robin"])
        fflux = os.path.join(template_path, flux_model)
        fstats_T = os.path.join(template_path, stats_T_model)

    # if model != 'mag' and model != 'mag_hcurl' and model != 'mqs' and model != 'mqs_hcurl':
    stats_Power_model = appcfg[method][time][geom][model]["stats_Power"]
    stats_Current_model = appcfg[method][time][geom][model]["stats_Current"]

    fstats_Power = os.path.join(template_path, stats_Power_model)
    fstats_Current = os.path.join(template_path, stats_Current_model)

    material_generic_def = ["conductor", "insulator"]
    if time == "transient":
        material_generic_def.append("conduct-nosource")  # only for transient with mqs

    dict = {
        "cfg": fcfg,
        "model": fmodel,
        "conductor": fconductor,
        "insulator": finsulator,
        "stats": [],
        "material_def": material_generic_def
    }

    if 'th' in model:
        dict["cooling"] = fcooling
        dict["robin"] = frobin
        dict["flux"] = fflux
        dict["stats"].append(fstats_T)

    # if model != 'mag' and model != 'mag_hcurl' and model != 'mqs' and model != 'mqs_hcurl':
    dict["stats"].append(fstats_Power)
    dict["stats"].append(fstats_Current)

    if check_templates(dict):
        pass

    return dict