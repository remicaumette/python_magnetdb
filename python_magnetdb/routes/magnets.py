from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from ..config import templates
from ..database import engine
from ..models import Magnet

router = APIRouter()


@router.get("/magnets.html", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('magnets.html', {"request": request})


@router.get("/magnets", response_class=HTMLResponse)
def index(request: Request):
    with Session(engine) as session:
        statement = select(Magnet)
        magnets = session.exec(statement).all()
    return templates.TemplateResponse('magnets/index.html', {"request": request, "magnets": magnets})


@router.get("/magnets/{id}", response_class=HTMLResponse)
def show(request: Request, id: int):
    with Session(engine) as session:
        magnet = session.get(Magnet, id)
        data = magnet.dict()
        data.pop('id', None)
        data["MParts"] = []
        for magnet in magnet.mparts:
            data["MParts"].append(magnet.name)
        return templates.TemplateResponse('magnets/show.html', {"request": request, "magnet": data})
