from os import path

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=f"{path.dirname(__file__)}/templates")
static_files = StaticFiles(directory=f"{path.dirname(__file__)}/static")
