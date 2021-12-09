from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

from ..config import templates
from ..forms import GeomForm

import yaml

router = APIRouter()

@router.get("/geoms.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('geoms.html', {"request": request})


@router.get("/geoms", response_class=HTMLResponse)
def index(request: Request):
    print("geom/index")
    geoms = {}
    desc = {}
    return templates.TemplateResponse('geoms/index.html', {
        "request": request,
        "geoms": geoms,
        "descriptions": desc
        })


@router.get("/geoms/{gname}", response_class=HTMLResponse)
def show(request: Request, gname: str):
    print("geom/show:", gname)
    # TODO where to get name filename
    # # load yaml file into data
    import os
    print("geom/show:", os.getcwd())

    import json
    # from python_magnetgeo import Helix
    geom = yaml.load(open("data/" + gname + ".yaml", 'r'), Loader = yaml.FullLoader)
    print("geom:", geom)
    data = json.loads(geom.to_json())
    print("data:", data, type(data))

    # re-organize data
    data.pop('__classname__')
    if 'materials' in data: data.pop('materials')
    for key in data:
        if isinstance(data[key], dict):
            if '__classname__' in data[key]:
                data[key].pop('__classname__')

    # TODO for Helices discard pitch, replace turns by actual number of turns
    return templates.TemplateResponse('geoms/show.html', {"request": request, "geom": data, "gname": gname})

@router.get("/geoms/{gname}/edit", response_class=HTMLResponse, name='edit_geom')
async def edit(request: Request, gname: str):
    print("geom/edit:", gname)
    # TODO load geom from filename==name
    geom = yaml.load(open("data/" + gname + ".yaml", 'r'))
    form = GeomForm(obj=geom, request=request)
    return templates.TemplateResponse('geoms/edit.html', {
        "id": id,
        "request": request,
        "form": form,
    })

@router.post("/geoms/{gname}/edit", response_class=HTMLResponse, name='update_geom')
async def update(request: Request, gname: str):
    print("geom/update:", gname)
    form = await GeomForm.from_formdata(request)
    if form.validate_on_submit():
        return RedirectResponse(router.url_path_for('geom', id=id), status_code=303)
    else:
        return templates.TemplateResponse('geom/edit.html', {
            "id": id,
            "request": request,
            "form": form,
        })
