from fastapi.templating import Jinja2Templates
from os import path

templates = Jinja2Templates(directory="{}/templates".format(path.dirname(__file__)))
