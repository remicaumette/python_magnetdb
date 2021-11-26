from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from sqlmodel import Session, select

from ..config import templates
from ..database import engine
from ..models import Magnet, MagnetUpdate 
from ..models import MSite, MSiteUpdate 

router = APIRouter()


@router.get("/msites.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('msites.html', {"request": request})


@router.get("/sites", response_class=HTMLResponse)
def index(request: Request):
    with Session(engine) as session:
        statement = select(MSite)
        msites = session.exec(statement).all()
    return templates.TemplateResponse('sites/index.html', {"request": request, "msites": msites})


@router.get("/sites/{id}", response_class=HTMLResponse)
def show(request: Request, id: int):
    with Session(engine) as session:
        msite = session.get(MSite, id)
        data = msite.dict()
        print("blueprint:", data)
        data.pop('id', None)
        data["Magnets"] = []
        for magnet in msite.magnets:
            data["Magnets"].append(magnet.name)
        return templates.TemplateResponse('sites/show.html', {"request": request, "msite": data})
        
MSiteUpdate.update_forward_refs()
