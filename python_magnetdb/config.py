from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from os import path

templates = Jinja2Templates(directory=f"{path.dirname(__file__)}/templates")
static_files = StaticFiles(directory=f"{path.dirname(__file__)}/static")
