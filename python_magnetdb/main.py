from fastapi import FastAPI

from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, escape, request
from fastapi.staticfiles import StaticFiles
from . import flask_routers
from os import path

flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = "powerful secretkey"
flask_app.config['WTF_CSRF_SECRET_KEY'] = "a csrf secret key"

flask_app.register_blueprint(flask_routers.urls_blueprint)

from .routes.home import router as home_router
from .routes.magnets import router as magnets_router
from .routes.materials import router as materials_router
from .routes.api.materials import router as api_materials_router
from .routes.api.parts import router as api_parts_router
from .routes.api.sites import router as api_sites_router
from .routes.api.magnets import router as api_magnets_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="{}/static".format(path.dirname(__file__))), name="static")

app.include_router(home_router)
app.include_router(magnets_router)
app.include_router(materials_router)
app.include_router(api_materials_router)
app.include_router(api_parts_router)
app.include_router(api_sites_router)
app.include_router(api_magnets_router)

# app.mount("/", WSGIMiddleware(flask_app))
