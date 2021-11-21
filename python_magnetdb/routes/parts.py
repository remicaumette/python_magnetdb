from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from ..config import templates
from ..database import engine
from ..models import MPart, Material

router = APIRouter()


@router.get("/mparts.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('mparts.html', {"request": request})


@router.get("/parts", response_class=HTMLResponse)
def index(request: Request):
    with Session(engine) as session:
        statement = select(MPart)
        mparts = session.exec(statement).all()
    return templates.TemplateResponse('parts/index.html', {"request": request, "mparts": mparts})


@router.get("/parts/{id}", response_class=HTMLResponse)
def show(request: Request, id: int):
    with Session(engine) as session:
        mpart = session.get(MPart, id)
        data = mpart.dict()
        data.pop('id', None)
        data['Material'] = session.get(Material, mpart.material_id).name
        data.pop('material_id', None)
        return templates.TemplateResponse('parts/show.html', {"request": request, "mpart": data})
