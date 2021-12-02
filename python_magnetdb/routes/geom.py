from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

from ..config import templates

router = APIRouter()


@router.get("/geoms.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('geoms.html', {"request": request})


@router.get("/geoms", response_class=HTMLResponse)
def index(request: Request):
    geoms = {}
    desc = {}
    return templates.TemplateResponse('geoms/index.html', {
        "request": request, 
        "geoms": geoms,
        "descriptions": desc
        })


@router.get("/geoms/{name}", response_class=HTMLResponse)
def show(request: Request, name: str):
    # TODO where to get name filename
    # # load yaml file into data
    data = {}
    return templates.TemplateResponse('geoms/show.html', {"request": request, "geom": data})

@router.get("/geoms/{name}/edit", response_class=HTMLResponse, name='edit_geom')
async def edit(request: Request, name: str):
    form = GeomForm(obj=geom, request=request)
    return templates.TemplateResponse('geoms/edit.html', {
        "id": id,
        "request": request,
        "form": form,
    })

@router.post("/geoms/{name}/edit", response_class=HTMLResponse, name='update_geom')
async def update(request: Request, name: str):
    form = await GeomForm.from_formdata(request)
    if form.validate_on_submit():
        return RedirectResponse(router.url_path_for('geom', id=id), status_code=303)
    else:
        return templates.TemplateResponse('geom/edit.html', {
            "id": id,
            "request": request,
            "form": form,
        })
