from fastapi import Request
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse

from ..config import templates

router = APIRouter()


@router.get("/magnets.html", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('magnets.html', {"request": request})
