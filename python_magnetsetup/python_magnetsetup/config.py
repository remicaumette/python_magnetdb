from typing import List, Optional

import os
import json

from .machines import load_machines


class appenv():

    def __init__(self, debug: bool = False):
        self.url_api: str = None
        self.yaml_repo: Optional[str] = None
        self.cad_repo: Optional[str] = None
        self.mesh_repo: Optional[str] = None
        self.template_repo: Optional[str] = None
        self.simage_repo: Optional[str] = None
        self.mrecord_repo: Optional[str] = None
        self.optim_repo: Optional[str] = None

        from decouple import Config, RepositoryEnv
        envdata = RepositoryEnv("settings.env")
        data = Config(envdata)
        if debug:
            print("appenv:", RepositoryEnv("settings.env").data)

        self.url_api = data.get('URL_API')
        self.compute_server = data.get('COMPUTE_SERVER')
        self.visu_server = data.get('VISU_SERVER')
        if 'TEMPLATE_REPO' in envdata:
            self.template_repo = data.get('TEMPLATE_REPO')
        if 'SIMAGE_REPO' in envdata:
            self.simage_repo = data.get('SIMAGE_REPO')
        if 'DATA_REPO' in envdata:
            self.yaml_repo = data.get('DATA_REPO') + "/geometries"
            self.cad_repo = data.get('DATA_REPO') + "/cad"
            self.mesh_repo = data.get('DATA_REPO') + "/meshes"
            self.mrecord_repo = data.get('DATA_REPO') + "/mrecords"
            self.optim_repo = data.get('DATA_REPO') + "/optims"
        print(f"DATA: {self.yaml_repo}")

    def template_path(self, debug: bool = False):
        """
        returns template_repo
        """
        if not self.template_repo:
            default_path = os.path.dirname(os.path.abspath(__file__))
            repo = os.path.join(default_path, "templates")
        else:
            repo = self.template_repo

        if debug:
            print("appenv/template_path:", repo)
        return repo

    def simage_path(self, debug: bool = False):
        """
        returns simage_repo
        """
        if not self.simage_repo:
            repo = os.path.join("/home/singularity")
        else:
            repo = self.simage_repo

        if debug:
            print("appenv/simage_path:", repo)
        return repo


def load_internal_config(path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'magnetsetup.json')):
    """
    Load app config (aka magnetsetup.json)
    """
    with open(path, 'r') as config:
        return json.load(config)
    raise Exception("Could not load magnetsetup.json")


def loadmachine(server: str):
    """
    Load app server config (aka machines.json)
    """

    server_defs = load_machines()
    if server in server_defs:
        return server_defs[server]
    else:
        raise ValueError(f"loadmachine: {server} no such server defined")
    pass


def check_templates(templates: dict):
    """
    check if template file exist
    """
    print("\n\n=== Checking Templates ===")
    for key in templates:
        if isinstance(templates[key], str):
            print(key, templates[key])
            with open(templates[key], "r") as f:
                pass

        elif isinstance(templates[key], str):
            for s in templates[key]:
                print(key, s)
                with open(s, "r") as f: pass
    print("==========================\n\n")

    return True


def supported_models(Appcfg, method: str, geom: str, time: str) -> List:
    """
    get supported models by method as a dict
    """

    models = []
    print("supported_models:", Appcfg[method])
    if Appcfg[method][time]:
        if geom in Appcfg[method][time]:
            for key in Appcfg[method][time][geom]:
                models.append(key)

    return models


def supported_methods(Appcfg) -> List:
    """
    get supported methods as a dict
    """

    methods = []
    for key in Appcfg:
        if Appcfg[key] and not key in ['mesh']:
            methods.append(key)

    return methods
